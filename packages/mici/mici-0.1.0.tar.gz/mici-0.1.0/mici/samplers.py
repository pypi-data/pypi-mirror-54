"""Monte Carlo sampler classes for peforming inference."""

import os
import logging
import tempfile
import signal
from collections import OrderedDict
import numpy as np
import mici
import mici.transitions as trans
from mici.states import ChainState
from mici.utils import get_size, get_valid_filename

try:
    import tqdm
    import tqdm.auto as tqdm_auto
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
try:
    import randomgen
    RANDOMGEN_AVAILABLE = True
except ImportError:
    RANDOMGEN_AVAILABLE = False
# Preferentially import Pool from multiprocess library if available as able
# to serialise much wider range of types including autograd functions
try:
    from multiprocess import Pool
except ImportError:
    from multiprocessing import Pool


logger = logging.getLogger(__name__)


def _ignore_sigint_initialiser():
    """Initialiser for multi-process workers to force ignoring SIGINT."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)


class MarkovChainMonteCarloMethod(object):
    """Generic Markov chain Monte Carlo (MCMC) sampler.

    Generates a Markov chain from some initial state by iteratively applying
    a sequence of Markov transition operators.
    """

    def __init__(self, rng, transitions):
        """
        Args:
            rng: Numpy RandomState random number generator instance.
            transitions: Ordered dictionary of Markov chain transitions to
                sequentially sample from on each chain iteration.
        """
        self.rng = rng
        self.transitions = transitions

    def _generate_memmap_filename(self, dir_path, prefix, key, index):
        key_str = get_valid_filename(str(key))
        if index is None:
            index = 0
        return os.path.join(dir_path, f'{prefix}_{index}_{key_str}.npy')

    def _open_new_memmap(self, filename, shape, dtype, default_val):
        memmap = np.lib.format.open_memmap(
            filename, dtype=dtype, mode='w+', shape=shape)
        memmap[:] = default_val
        return memmap

    def _memmaps_to_filenames(self, obj):
        if isinstance(obj, np.memmap):
            return obj.filename
        elif isinstance(obj, dict):
            return {k: self._memmaps_to_filenames(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._memmaps_to_filenames(v) for v in obj]

    def _init_chain_stats(self, n_sample, memmap_enabled, memmap_path,
                          chain_index):
        chain_stats = {}
        for trans_key, trans in self.transitions.items():
            chain_stats[trans_key] = {}
            if hasattr(trans, 'statistic_types'):
                for key, (dtype, val) in trans.statistic_types.items():
                    if memmap_enabled:
                        filename = self._generate_memmap_filename(
                            memmap_path, 'stats', f'{trans_key}_{key}',
                            chain_index)
                        chain_stats[trans_key][key] = self._open_new_memmap(
                            filename, (n_sample,), dtype, val)
                    else:
                        chain_stats[trans_key][key] = np.full(
                            n_sample, val, dtype)
        return chain_stats

    def _sample_chain(self, rng, n_sample, init_state, trace_funcs,
                      chain_index, parallel_chains, memmap_enabled=False,
                      memmap_path=None, monitor_stats=None):
        for trans_key, transition in self.transitions.items():
            for var_key in transition.state_variables:
                if var_key not in init_state:
                    raise ValueError(
                        f'init_state does contain have {var_key} value '
                        f'required by {trans_key} transition.')
        if not isinstance(init_state, (ChainState, dict)):
            raise TypeError(
                'init_state should be a dictionary or `ChainState`.')
        state = (ChainState(**init_state) if isinstance(init_state, dict)
                 else init_state)
        chain_stats = self._init_chain_stats(
            n_sample, memmap_enabled, memmap_path, chain_index)
        # Initialise chain trace arrays
        traces = {}
        for trace_func in trace_funcs:
            for key, val in trace_func(state).items():
                val = np.array(val) if np.isscalar(val) else val
                init = np.nan if np.issubdtype(val.dtype, np.inexact) else 0
                if memmap_enabled:
                    filename = self._generate_memmap_filename(
                        memmap_path, 'trace', key, chain_index)
                    traces[key] = self._open_new_memmap(
                        filename, (n_sample,) + val.shape, val.dtype, init)
                else:
                    traces[key] = np.full(
                        (n_sample,) + val.shape, init, val.dtype)
        total_return_nbytes = get_size(chain_stats) + get_size(traces)
        # Check if running in parallel and if total number of bytes to be
        # returned exceeds pickle limit
        if parallel_chains and total_return_nbytes > 2**31 - 1:
            raise RuntimeError(
                f'Total number of bytes allocated for arrays to be returned '
                f'({total_return_nbytes / 2**30:.2f} GiB) exceeds size limit '
                f'for returning results of a process (2 GiB). Try rerunning '
                f'with chain memory-mapping enabled (`memmap_enabled=True`).')
        if TQDM_AVAILABLE:
            kwargs = {
                'desc': f'Chain {0 if chain_index is None else chain_index}',
                'unit': 'it',
                'dynamic_ncols': True,
            }
            if parallel_chains:
                sample_range = tqdm_auto.trange(
                    n_sample, **kwargs, position=chain_index)
            else:
                sample_range = tqdm.trange(n_sample, **kwargs)
        else:
            sample_range = range(n_sample)
        try:
            for sample_index in sample_range:
                for trans_key, transition in self.transitions.items():
                    state, trans_stats = transition.sample(state, rng)
                    if trans_stats is not None:
                        if trans_key not in chain_stats:
                            logger.warning(
                                f'Transition {trans_key} returned statistics '
                                f'but has no `statistic_types` attribute.')
                        for key, val in trans_stats.items():
                            if key in chain_stats[trans_key]:
                                chain_stats[trans_key][key][sample_index] = val
                for trace_func in trace_funcs:
                    for key, val in trace_func(state).items():
                        traces[key][sample_index] = val
                if TQDM_AVAILABLE and monitor_stats is not None:
                    postfix_stats = {}
                    for (trans_key, stats_key) in monitor_stats:
                        if (trans_key not in chain_stats or
                                stats_key not in chain_stats[trans_key]):
                            logger.warning(
                                f'Statistics key pair {(trans_key, stats_key)}'
                                f' to be monitored is not valid.')
                        print_key = f'mean({stats_key})'
                        postfix_stats[print_key] = np.mean(
                            chain_stats[trans_key][stats_key][:sample_index+1])
                    sample_range.set_postfix(postfix_stats)
        except KeyboardInterrupt:
            if memmap_enabled:
                for trace in traces.values():
                    trace.flush()
                for trans_stats in chain_stats.values():
                    for stat in trans_stats.values():
                        stat.flush()
        else:
            # If not interrupted increment sample_index so that it equals
            # n_sample to flag chain completed sampling
            sample_index += 1
        if parallel_chains and memmap_enabled:
                trace_filenames = self._memmaps_to_filenames(traces)
                stats_filenames = self._memmaps_to_filenames(chain_stats)
                return trace_filenames, stats_filenames, sample_index
        return state, traces, chain_stats, sample_index

    def __preprocess_kwargs(self, kwargs):
        if 'memmap_enabled' not in kwargs:
            kwargs['memmap_enabled'] = False
        # Create temporary directory if memory mapping and no path provided
        if kwargs['memmap_enabled'] and 'memmap_path' not in kwargs:
            kwargs['memmap_path'] = tempfile.mkdtemp()
        return kwargs

    def sample_chain(self, n_sample, init_state, trace_funcs, **kwargs):
        """Sample a Markov chain from a given initial state.

        Performs a specified number of chain iterations (each of which may be
        composed of multiple individual Markov transitions), recording the
        outputs of functions of the sampled chain state after each iteration.

        Args:
            n_sample (int): Number of samples (iterations) to draw per chain.
            init_state (ChainState or dict): Initial chain state. Either a
                `ChainState` object or a dictionary with entries specifying
                initial values for all state variables used by chain
                transition `sample` methods.
            trace_funcs (Iterable[callable]): List of functions which compute
                the variables to be recorded at each chain iteration, with each
                trace function being passed the current state and returning a
                dictionary of scalar or array values corresponding to the
                variable(s) to be stored. The keys in the returned dictionaries
                are used to index the trace arrays in the returned traces
                dictionary. If a key appears in multiple dictionaries only the
                the value corresponding to the last trace function to return
                that key will be stored.

        Kwargs:
            memmap_enabled (bool): Whether to memory-map arrays used to store
                chain data to files on disk to avoid excessive system memory
                usage for long chains and/or large chain states. The chain data
                is written to `.npy` files in the directory specified by
                `memmap_path` (or a temporary directory if not provided). These
                files persist after the termination of the function so should
                be manually deleted when no longer required. Default is to
                for memory mapping to be disabled.
            memmap_path (str): Path to directory to write memory-mapped chain
                data to. If not provided, a temporary directory will be created
                and the chain data written to files there.
            monitor_stats (Iterable[tuple(str, str)]): List of tuples of string
                key pairs, with first entry the key of a Markov transition in
                the `transitions` dict passed to the the `__init__` method and
                the second entry the key of a chain statistic that will be
                returned in the `chain_stats` dictionary. The mean over samples
                computed so far of the chain statistics associated with any
                valid key-pairs will be monitored during sampling  by printing
                as postfix to progress bar (if `tqdm` is installed).

        Returns:
            final_state (ChainState): State of chain after final iteration. May
                be used to resume sampling a chain by passing as the initial
                state to a new `sample_chain` call.
            traces (dict[str, array]): Dictionary of chain trace arrays. Values
                in dictionary are arrays of variables outputted by trace
                functions in `trace_funcs` with leading dimension of array
                corresponding to the sampling (draw) index. The key for each
                value is the corresponding key in the dictionary returned by
                the trace function which computed the traced value.
            chain_stats (dict[str, dict[str, array]]): Dictionary of chain
                transition statistic dictionaries. Values in outer dictionary
                are dictionaries of statistics for each chain transition, keyed
                by the string key for the transition. The values in each inner
                transition dictionary are arrays of chain statistic values with
                the leading dimension of each array corresponding to the
                sampling (draw) index. The key for each value is a string
                description of the corresponding integration transition
                statistic.
        """
        kwargs = self.__preprocess_kwargs(kwargs)
        final_state, traces, chain_stats, sample_index = self._sample_chain(
            rng=self.rng, n_sample=n_sample, init_state=init_state,
            trace_funcs=trace_funcs, chain_index=None, parallel_chains=False,
            **kwargs)
        if sample_index != n_sample:
            # Sampling interrupted therefore truncate returned arrays
            # Using resize methods makes agnostic to whether array is
            # memory mapped or not
            for trans_stats in chain_stats.values():
                for key in trans_stats:
                    trans_stats[key].resize(
                        (sample_index,) + trans_stats[key].shape[1:])
            for key in traces:
                traces[key].resize(
                    (sample_index,) + traces[key].shape[1:])
            logger.error(
                f'Sampling manually interrupted at iteration {sample_index}. '
                f'Arrays containing chain traces and statistics computed '
                f'before interruption will be returned.')
        return final_state, traces, chain_stats

    def _collate_chain_outputs(self, n_sample, chain_outputs, load_memmaps):
        final_states_stack = []
        traces_stack = {}
        n_chain = len(chain_outputs)
        chain_stats_stack = {}
        for chain_index, chain_output in enumerate(chain_outputs):
            final_state, traces, chain_stats, sample_index = chain_output
            final_states_stack.append(final_state)
            for key, val in traces.items():
                if load_memmaps:
                    val = np.lib.format.open_memmap(val)
                if sample_index != n_sample:
                    # Sampling interrupted therefore truncate returned arrays
                    # Using resize methods makes agnostic to whether array is
                    # memory mapped or not
                    val.resize((sample_index,) + val.shape[1:], refcheck=False)
                if chain_index == 0:
                    traces_stack[key] = [val]
                else:
                    traces_stack[key].append(val)
            for trans_key, trans_stats in chain_stats.items():
                if chain_index == 0:
                    chain_stats_stack[trans_key] = {}
                for key, val in trans_stats.items():
                    if load_memmaps:
                        val = np.lib.format.open_memmap(val)
                    if sample_index != n_sample:
                        # Sampling interrupted therefore truncate returned
                        # arrays Using resize methods makes agnostic to whether
                        # array is memory mapped or not
                        val.resize((sample_index,) + val.shape[1:],
                                   refcheck=False)
                    if chain_index == 0:
                        chain_stats_stack[trans_key][key] = [val]
                    else:
                        chain_stats_stack[trans_key][key].append(val)
        return final_states_stack, traces_stack, chain_stats_stack

    def sample_chains(self, n_sample, init_states, trace_funcs, n_process=1,
                      **kwargs):
        """Sample one or more Markov chains from given initial states.

        Performs a specified number of chain iterations (each of which may be
        composed of multiple individual Markov transitions), recording the
        outputs of functions of the sampled chain state after each iteration.
        The chains may be run in parallel across multiple independent processes
        or sequentially. In all cases all chains use independent random draws.

        Args:
            n_sample (int): Number of samples (iterations) to draw per chain.
            init_states (Iterable[ChainState] or Iterable[dict]): Initial
                chain states. Each entry can be either a `ChainState` object or
                a dictionary with entries specifying initial values for all
                state variables used by chain transition `sample` methods.
            trace_funcs (Iterable[callable]): List of functions which compute
                the variables to be recorded at each chain iteration, with each
                trace function being passed the current state and returning a
                dictionary of scalar or array values corresponding to the
                variable(s) to be stored. The keys in the returned dictionaries
                are used to index the trace arrays in the returned traces
                dictionary. If a key appears in multiple dictionaries only the
                the value corresponding to the last trace function to return
                that key will be stored.
            n_process (int or None): Number of parallel processes to run chains
                over. If set to one then chains will be run sequentially in
                otherwise a `multiprocessing.Pool` object will be used to
                dynamically assign the chains across multiple processes. If
                set to `None` then the number of processes will default to the
                output of `os.cpu_count()`.

        Kwargs:
            memmap_enabled (bool): Whether to memory-map arrays used to store
                chain data to files on disk to avoid excessive system memory
                usage for long chains and/or large chain states. The chain data
                is written to `.npy` files in the directory specified by
                `memmap_path` (or a temporary directory if not provided). These
                files persist after the termination of the function so should
                be manually deleted when no longer required. Default is to
                for memory mapping to be disabled.
            memmap_path (str): Path to directory to write memory-mapped chain
                data to. If not provided, a temporary directory will be created
                and the chain data written to files there.
            monitor_stats (Iterable[tuple(str, str)]): List of tuples of string
                key pairs, with first entry the key of a Markov transition in
                the `transitions` dict passed to the the `__init__` method and
                the second entry the key of a chain statistic that will be
                returned in the `chain_stats` dictionary. The mean over samples
                computed so far of the chain statistics associated with any
                valid key-pairs will be monitored during sampling  by printing
                as postfix to progress bar (if `tqdm` is installed).

        Returns:
            final_states (list[ChainState]): States of chains after final
                iteration. May be used to resume sampling a chain by passing as
                the initial states to a new `sample_chains` call.
            traces (dict[str, list[array]]): Dictionary of chain trace arrays.
                Values in dictionary are list of arrays of variables outputted
                by trace functions in `trace_funcs` with each array in the list
                corresponding to a single chain and the leading dimension of
                each array corresponding to the sampling (draw) index. The key
                for each value is the corresponding key in the dictionary
                returned by the trace function which computed the traced value.
            chain_stats (dict[str, dict[str, list[array]]]): Dictionary of
                chain transition statistic dictionaries. Values in outer
                dictionary are dictionaries of statistics for each chain
                transition, keyed by the string key for the transition. The
                values in each inner transition dictionary are lists of arrays
                of chain statistic values with each array in the list
                corresponding to a single chain and the leading dimension of
                each array corresponding to the sampling (draw) index. The key
                for each value is a string description of the corresponding
                integration transition statistic.
        """
        n_chain = len(init_states)
        kwargs = self.__preprocess_kwargs(kwargs)
        if RANDOMGEN_AVAILABLE:
            seed = self.rng.randint(2**64, dtype='uint64')
            rngs = [randomgen.Xorshift1024(seed).jump(i).generator
                    for i in range(n_chain)]
        else:
            seeds = (self.rng.choice(2**16, n_chain, False) * 2**16 +
                     self.rng.choice(2**16, n_chain, False))
            rngs = [np.random.RandomState(seed) for seed in seeds]
        chain_outputs = []
        shared_kwargs_list = [{
                'rng': rng,
                'n_sample': n_sample,
                'init_state': init_state,
                'trace_funcs': trace_funcs,
                'chain_index': c,
                **kwargs
            } for c, (rng, init_state) in enumerate(zip(rngs, init_states))]
        if n_process == 1:
            # Using single process therefore run chains sequentially
            for c, shared_kwargs in enumerate(shared_kwargs_list):
                final_state, traces, stats, sample_index = self._sample_chain(
                    **shared_kwargs, parallel_chains=False)
                chain_outputs.append(
                    (final_state, traces, stats, sample_index))
                if sample_index != n_sample:
                    logger.error(
                        f'Sampling manually interrupted at chain {c} iteration'
                        f' {sample_index}. Arrays containing chain traces'
                        f' and statistics computed before interruption will'
                        f' be returned.')
                    break
        else:
            # Run chains in parallel using a multiprocess(ing).Pool
            # Child processes made to ignore SIGINT signals to allow handling
            # of KeyboardInterrupts in parent process
            n_completed = 0
            pool = Pool(n_process, _ignore_sigint_initialiser)
            try:
                results = [
                    pool.apply_async(
                        self._sample_chain,
                        kwds=dict(**shared_kwargs, parallel_chains=True))
                    for shared_kwargs in shared_kwargs_list]
                for result in results:
                    chain_outputs.append(result.get())
                    n_completed += 1
            except KeyboardInterrupt:
                # Close any still running processes
                pool.terminate()
                pool.join()
                err_message = 'Sampling manually interrupted.'
                if n_completed > 0:
                    err_message += (
                        f' Data for {n_completed} completed chains will be '
                        f'returned.')
                if kwargs['memmap_enabled']:
                    err_message += (
                        f' All data recorded so far including in progress '
                        f'chains is available in directory '
                        f'{kwargs["memmap_path"]}.')
                logger.error(err_message)
        # When running parallel jobs with memory-mapping enabled, data arrays
        # returned by processes as file paths to array memory-maps therfore
        # load memory-maps objects from file before returing results
        load_memmaps = kwargs['memmap_enabled'] and n_process > 1
        return self._collate_chain_outputs(
            n_sample, chain_outputs, load_memmaps)


class HamiltonianMCMC(MarkovChainMonteCarloMethod):
    """Wrapper class for Hamiltonian Markov chain Monte Carlo (H-MCMC) methods.

    Here H-MCMC is defined as a MCMC method which augments the original target
    variable (henceforth position variable) with a momentum variable with a
    user specified conditional distribution given the position variable. In
    each chain iteration two Markov transitions leaving the resulting joint
    distribution on position and momentum variables invariant are applied -
    the momentum variables are updated in a transition which leaves their
    conditional distribution invariant (momentum transition) and then a
    trajectory in the joint space is generated by numerically integrating a
    Hamiltonian dynamic with an appropriate symplectic integrator which is
    exactly reversible, volume preserving and approximately conserves the joint
    probability density of the target-momentum state pair; one state from the
    resulting trajectory is then selected as the next joint chain state using
    an appropriate sampling scheme such that the joint distribution is left
    exactly invariant (integration transition).

    There are various options available for both the momentum transition and
    integration transition, with by default the momentum transition set to be
    independent resampling of the momentum variables from their conditional
    distribution.

    References:

      1. Duane, S., Kennedy, A.D., Pendleton, B.J. and Roweth, D., 1987.
         Hybrid Monte Carlo. Physics letters B, 195(2), pp.216-222.
      2. Neal, R.M., 2011. MCMC using Hamiltonian dynamics.
         Handbook of Markov Chain Monte Carlo, 2(11), p.2.
    """

    def __init__(self, system, rng, integration_transition,
                 momentum_transition=None):
        """
        Args:
            system: Hamiltonian system to be simulated.
            rng: Numpy RandomState random number generator instance.
            integration_transition: Markov transition operator which jointly
                updates the position and momentum components of the chain
                state by integrating the Hamiltonian dynamics of the system
                to propose new values for the state.
            momentum_transition: Markov transition operator which updates only
                the momentum component of the chain state. If set to `None` a
                transition operator which independently samples the momentum
                from its conditional distribution will be used.
        """
        self.system = system
        self.rng = rng
        if momentum_transition is None:
            momentum_transition = trans.IndependentMomentumTransition(system)
        super().__init__(rng, OrderedDict(
            momentum_transition=momentum_transition,
            integration_transition=integration_transition))

    def _preprocess_init_state(self, init_state):
        """Make sure initial state is a ChainState and has momentum."""
        if isinstance(init_state, np.ndarray):
            # If array use to set position component of new ChainState
            init_state = ChainState(pos=init_state, mom=None, dir=1)
        elif not isinstance(init_state, ChainState) or 'mom' not in init_state:
            raise TypeError(
                'init_state should be an array or `ChainState` with '
                '`mom` attribute.')
        if init_state.mom is None:
            init_state.mom = self.system.sample_momentum(init_state, self.rng)
        return init_state

    def __preprocess_kwargs(self, kwargs):
        # default to tracing only position component of state
        if 'trace_funcs' not in kwargs:
            kwargs['trace_funcs'] = [lambda state: {'pos': state.pos}]
        # if `monitor_stats` specified, expand all statistics keys to key pairs
        # with transition key set to `integration_transition`
        if 'monitor_stats' in kwargs:
            kwargs['monitor_stats'] = [
                ('integration_transition', stats_key)
                for stats_key in kwargs['monitor_stats']]
        else:
            kwargs['monitor_stats'] = [
                ('integration_transition', 'accept_prob')]
        return kwargs

    def sample_chain(self, n_sample, init_state, **kwargs):
        """Sample a Markov chain from a given initial state.

        Performs a specified number of chain iterations (each of which may be
        composed of multiple individual Markov transitions), recording the
        outputs of functions of the sampled chain state after each iteration.

        Args:
            n_sample (int): Number of samples (iterations) to draw per chain.
            init_state (ChainState or array): Initial chain state. The state
                can be either an array specifying the state position component
                or a `ChainState` instance. If an array is passed or the `mom`
                attribute of the state is not set, a momentum component will be
                independently sampled from its conditional distribution.

        Kwargs:
            trace_funcs (Iterable[callable]): List of functions which compute
                the variables to be recorded at each chain iteration, with each
                trace function being passed the current state and returning a
                dictionary of scalar or array values corresponding to the
                variable(s) to be stored. The keys in the returned dictionaries
                are used to index the trace arrays in the returned traces
                dictionary. If a key appears in multiple dictionaries only the
                the value corresponding to the last trace function to return
                that key will be stored. Default is for a single trace function
                which records the `pos` component of the state.
            memmap_enabled (bool): Whether to memory-map arrays used to store
                chain data to files on disk to avoid excessive system memory
                usage for long chains and/or large chain states. The chain data
                is written to `.npy` files in the directory specified by
                `memmap_path` (or a temporary directory if not provided). These
                files persist after the termination of the function so should
                be manually deleted when no longer required. Default is to
                for memory mapping to be disabled.
            memmap_path (str): Path to directory to write memory-mapped chain
                data to. If not provided, a temporary directory will be created
                and the chain data written to files there.
            monitor_stats (Iterable[str]): List of string keys of chain
                statistics to monitor mean of over samples computed so far
                during sampling by printing as postfix to progress bar (if
                `tqdm` is installed). Default is to print only the mean
                `accept_prob` statistic.

        Returns:
            final_state (ChainState): State of chain after final iteration. May
                be used to resume sampling a chain by passing as the initial
                state to a new `sample_chain` call.
            traces (dict[str, array]): Dictionary of chain trace arrays. Values
                in dictionary are arrays of variables outputted by trace
                functions in `trace_funcs` with leading dimension of array
                corresponding to the sampling (draw) index. The key for each
                value is the corresponding key in the dictionary returned by
                the trace function which computed the traced value.
            chain_stats (dict[str, array]): Dictionary of chain integration
                transition statistics. Values in dictionary are arrays of chain
                statistic values with the leading dimension of each array
                corresponding to the sampling (draw) index. The key for each
                value is a string description of the corresponding integration
                transition statistic.
        """
        init_state = self._preprocess_init_state(init_state)
        kwargs = self.__preprocess_kwargs(kwargs)
        final_state, traces, chain_stats = super().sample_chain(
            n_sample, init_state, **kwargs)
        chain_stats = chain_stats.get('integration_transition', {})
        return final_state, traces, chain_stats

    def sample_chains(self, n_sample, init_states, **kwargs):
        """Sample one or more Markov chains from given initial states.

        Performs a specified number of chain iterations (each of consists of a
        momentum transition and integration transition), recording the outputs
        of functions of the sampled chain state after each iteration. The
        chains may be run in parallel across multiple independent processes or
        sequentially. In all cases all chains use independent random draws.

        Args:
            n_sample (int): Number of samples (iterations) to draw per chain.
            init_states (Iterable[ChainState] or Iterable[array]): Initial
                chain states. Each state can be either an array specifying the
                state position component or a `ChainState` instance. If an
                array is passed or the `mom` attribute of the state is not set,
                a momentum component will be independently sampled from its
                conditional distribution. One chain will be run for each state
                in the iterable sequence.

        Kwargs:
            n_process (int or None): Number of parallel processes to run chains
                over. If set to one then chains will be run sequentially in
                otherwise a `multiprocessing.Pool` object will be used to
                dynamically assign the chains across multiple processes. If set
                to `None` then the number of processes will be set to the
                output of `os.cpu_count()`. Default is `n_process=1`.
            trace_funcs (Iterable[callable]): List of functions which compute
                the variables to be recorded at each chain iteration, with each
                trace function being passed the current state and returning a
                dictionary of scalar or array values corresponding to the
                variable(s) to be stored. The keys in the returned dictionaries
                are used to index the trace arrays in the returned traces
                dictionary. If a key appears in multiple dictionaries only the
                the value corresponding to the last trace function to return
                that key will be stored. Default is for a single trace function
                which records the `pos` component of the state.
            memmap_enabled (bool): Whether to memory-map arrays used to store
                chain data to files on disk to avoid excessive system memory
                usage for long chains and/or large chain states. The chain data
                is written to `.npy` files in the directory specified by
                `memmap_path` (or a temporary directory if not provided). These
                files persist after the termination of the function so should
                be manually deleted when no longer required. Default is to
                for memory mapping to be disabled.
            memmap_path (str): Path to directory to write memory-mapped chain
                data to. If not provided, a temporary directory will be created
                and the chain data written to files there.
            monitor_stats (Iterable[str]): List of string keys of chain
                statistics to monitor mean of over samples computed so far
                during sampling by printing as postfix to progress bar (if
                `tqdm` is installed). Default is to print only the mean
                `accept_prob` statistic.

        Returns:
            final_states (list[ChainState]): States of chains after final
                iteration. May be used to resume sampling a chain by passing as
                the initial states to a new `sample_chains` call.
            traces (dict[str, list[array]]): Dictionary of chain trace arrays.
                Values in dictionary are list of arrays of variables outputted
                by trace functions in `trace_funcs` with each array in the list
                corresponding to a single chain and the leading dimension of
                each array corresponding to the sampling (draw) index. The key
                for each value is the corresponding key in the dictionary
                returned by the trace function which computed the traced value.
            chain_stats (dict[str, list[array]]): Dictionary of chain
                integration transition statistics. Values in dictionary are
                lists of arrays of chain statistic values with each array in
                the list corresponding to a single chain and the leading
                dimension of each array corresponding to the sampling (draw)
                index. The key for each value is a string description of the
                corresponding integration transition statistic.
        """
        init_states = [self._preprocess_init_state(i) for i in init_states]
        kwargs = self.__preprocess_kwargs(kwargs)
        final_states, traces, chain_stats = super().sample_chains(
            n_sample, init_states, **kwargs)
        chain_stats = chain_stats.get('integration_transition', {})
        return final_states, traces, chain_stats


class StaticMetropolisHMC(HamiltonianMCMC):
    """Static integration time H-MCMC implementation with Metropolis sampling.

    In each transition a trajectory is generated by integrating the Hamiltonian
    dynamics from the current state in the current integration time direction
    for a fixed integer number of integrator steps.

    The state at the end of the trajectory with the integration direction
    negated (this ensuring the proposed move is an involution) is used as the
    proposal in a Metropolis acceptance step. The integration direction is then
    deterministically negated again irrespective of the accept decision, with
    the effect being that on acceptance the integration direction will be equal
    to its initial value and on rejection the integration direction will be
    the negation of its initial value.

    This is original proposed Hybrid Monte Carlo (often now instead termed
    Hamiltonian Monte Carlo) algorithm [1,2].

    References:

      1. Duane, S., Kennedy, A.D., Pendleton, B.J. and Roweth, D., 1987.
         Hybrid Monte Carlo. Physics letters B, 195(2), pp.216-222.
      2. Neal, R.M., 2011. MCMC using Hamiltonian dynamics.
         Handbook of Markov Chain Monte Carlo, 2(11), p.2.
    """

    def __init__(self, system, integrator, rng, n_step,
                 momentum_transition=None):
        integration_transition = trans.MetropolisStaticIntegrationTransition(
            system, integrator, n_step)
        super().__init__(system, rng, integration_transition,
                         momentum_transition)

    @property
    def n_step(self):
        return self.transitions['integration_transition'].n_step

    @n_step.setter
    def n_step(self, value):
        self.transitions['integration_transition'].n_step = value


class RandomMetropolisHMC(HamiltonianMCMC):
    """Random integration time H-MCMC with Metropolis sampling of new state.

    In each transition a trajectory is generated by integrating the Hamiltonian
    dynamics from the current state in the current integration time direction
    for a random integer number of integrator steps sampled from the uniform
    distribution on an integer interval.

    The state at the end of the trajectory with the integration direction
    negated (this ensuring the proposed move is an involution) is used as the
    proposal in a Metropolis acceptance step. The integration direction is then
    deterministically negated again irrespective of the accept decision, with
    the effect being that on acceptance the integration direction will be equal
    to its initial value and on rejection the integration direction will be
    the negation of its initial value.

    The randomisation of the number of integration steps avoids the potential
    of the chain mixing poorly due to using an integration time close to the
    period of (near) periodic systems [1,2].

    References:

      1. Neal, R.M., 2011. MCMC using Hamiltonian dynamics.
         Handbook of Markov Chain Monte Carlo, 2(11), p.2.
      2. Mackenzie, P.B., 1989. An improved hybrid Monte Carlo method.
         Physics Letters B, 226(3-4), pp.369-371.
    """

    def __init__(self, system, integrator, rng, n_step_range,
                 momentum_transition=None):
        integration_transition = trans.MetropolisRandomIntegrationTransition(
            system, integrator, n_step_range)
        super().__init__(system, rng, integration_transition,
                         momentum_transition)

    @property
    def n_step_range(self):
        return self.transitions['integration_transition'].n_step_range

    @n_step_range.setter
    def n_step_range(self, value):
        self.transitions['integration_transition'].n_step_range = value


class DynamicMultinomialHMC(HamiltonianMCMC):
    """Dynamic integration time H-MCMC with multinomial sampling of new state.

    In each transition a binary tree of states is recursively computed by
    integrating randomly forward and backward in time by a number of steps
    equal to the previous tree size [1,2] until a termination criteria on the
    tree leaves is met. The next chain state is chosen from the candidate
    states using a progressive multinomial sampling scheme [2] based on the
    relative probability densities of the different candidate states, with the
    resampling biased towards states further from the current state.

    References:

      1. Hoffman, M.D. and Gelman, A., 2014. The No-U-turn sampler:
         adaptively setting path lengths in Hamiltonian Monte Carlo.
         Journal of Machine Learning Research, 15(1), pp.1593-1623.
      2. Betancourt, M., 2017. A conceptual introduction to Hamiltonian Monte
         Carlo. arXiv preprint arXiv:1701.02434.
    """

    def __init__(self, system, integrator, rng,
                 max_tree_depth=10, max_delta_h=1000,
                 termination_criterion=trans.riemannian_no_u_turn_criterion,
                 momentum_transition=None):
        integration_transition = trans.MultinomialDynamicIntegrationTransition(
            system, integrator, max_tree_depth, max_delta_h,
            termination_criterion)
        super().__init__(system, rng, integration_transition,
                         momentum_transition)

    @property
    def max_tree_depth(self):
        return self.transitions['integration_transition'].max_tree_depth

    @max_tree_depth.setter
    def max_tree_depth(self, value):
        self.transitions['integration_transition'].max_tree_depth = value

    @property
    def max_delta_h(self):
        return self.transitions['integration_transition'].max_delta_h

    @max_delta_h.setter
    def max_delta_h(self, value):
        self.transitions['integration_transition'].max_delta_h = value
