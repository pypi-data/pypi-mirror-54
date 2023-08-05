"""Utility functions to run the Quantum Volume benchmark defined by IBM in
https://arxiv.org/abs/1811.12926.
"""

from typing import Optional, List, cast, Callable, Dict, Tuple
from dataclasses import dataclass

import numpy as np

import cirq
import cirq.contrib.routing as ccr


def generate_model_circuit(num_qubits: int,
                           depth: int,
                           *,
                           random_state: Optional[np.random.RandomState] = None
                          ) -> cirq.Circuit:
    """Generates a model circuit with the given number of qubits and depth.

    The generated circuit consists of `depth` layers of random qubit
    permutations followed by random two-qubit gates that are sampled from the
    Haar measure on SU(4).

    Args:
        num_qubits: The number of qubits in the generated circuit.
        depth: The number of layers in the circuit.
        random_state: A way to seed the RandomState.

    Returns:
        The generated circuit.
    """
    # Setup the circuit and its qubits.
    qubits = cirq.LineQubit.range(num_qubits)
    circuit = cirq.Circuit()
    if random_state is None:
        random_state = np.random

    # For each layer.
    for _ in range(depth):
        # Generate uniformly random permutation Pj of [0...n-1]
        perm = random_state.permutation(num_qubits)

        # For each consecutive pair in Pj, generate Haar random SU(4)
        # Decompose each SU(4) into CNOT + SU(2) and add to Ci
        for k in range(0, num_qubits - 1, 2):
            permuted_indices = [int(perm[k]), int(perm[k + 1])]
            special_unitary = cirq.testing.random_special_unitary(
                4, random_state=random_state)

            # Convert the decomposed unitary to Cirq operations and add them to
            # the circuit.
            circuit.append(
                cirq.TwoQubitMatrixGate(special_unitary).on(
                    qubits[permuted_indices[0]], qubits[permuted_indices[1]]))

    # Don't measure all of the qubits at the end of the circuit because we will
    # need to classically simulate it to compute its heavy set.
    return circuit


def compute_heavy_set(circuit: cirq.Circuit) -> List[int]:
    """Classically compute the heavy set of the given circuit.

    The heavy set is defined as the output bit-strings that have a greater than
    median probability of being generated.

    Args:
        circuit: The circuit to classically simulate.

    Returns:
        A list containing all of the heavy bit-string results.
    """
    # Classically compute the probabilities of each output bit-string through
    # simulation.
    simulator = cirq.Simulator()
    results = cast(cirq.WaveFunctionTrialResult,
                   simulator.simulate(program=circuit))

    # Compute the median probability of the output bit-strings. Note that heavy
    # output is defined in terms of probabilities, where our wave function is in
    # terms of amplitudes. We convert it by using the Born rule: squaring each
    # amplitude and taking their absolute value
    median = np.median(np.abs(results.state_vector()**2))

    # The output wave function is a vector from the result value (big-endian) to
    # the probability of that bit-string. Return all of the bit-string
    # values that have a probability greater than the median.
    return [
        idx for idx, amp in enumerate(results.state_vector())
        if np.abs(amp**2) > median
    ]


def sample_heavy_set(circuit: cirq.Circuit,
                     heavy_set: List[int],
                     *,
                     repetitions=10000,
                     sampler: cirq.Sampler = cirq.Simulator(),
                     mapping: Dict[cirq.ops.Qid, cirq.ops.Qid] = None) -> float:
    """Run a sampler over the given circuit and compute the percentage of its
       outputs that are in the heavy set.

    Args:
        circuit: The circuit to sample.
        heavy_set: The previously-computed heavy set for the given circuit.
        repetitions: The number of runs to sample the circuit.
        sampler: The sampler to run on the given circuit.
        mapping: An optional mapping from compiled qubits to original qubits,
            to maintain the ordering between the model and compiled circuits.

    Returns:
        A probability percentage, from 0 to 1, representing how many of the
        output bit-strings were in the heaby set.

    """
    # Add measure gates to the end of (a copy of) the circuit. Ensure that those
    # gates measure those in the given mapping, preserving this order.
    qubits = circuit.all_qubits()
    key = None
    if mapping:
        key = lambda q: mapping[q]
        qubits = frozenset(mapping.keys())
    circuit_copy = circuit + cirq.measure(*sorted(qubits, key=key))

    # Run the sampler to compare each output against the Heavy Set.
    measurements = sampler.run(program=circuit_copy, repetitions=repetitions)

    # Compute the number of outputs that are in the heavy set.
    num_in_heavy_set = np.sum(np.in1d(measurements.data.iloc[:, 0], heavy_set))

    # Return the number of Heavy outputs over the number of runs.
    return num_in_heavy_set / repetitions


def compile_circuit(
        circuit: cirq.Circuit,
        *,
        device: cirq.google.xmon_device.XmonDevice,
        compiler: Callable[[cirq.Circuit], cirq.Circuit] = None,
        routing_algo_name: Optional[str] = None,
        router: Optional[Callable[..., ccr.SwapNetwork]] = None,
) -> Tuple[cirq.Circuit, Dict[cirq.ops.Qid, cirq.ops.Qid]]:
    """Compile the given model circuit onto the given device. This uses a
    different compilation method than described in
    https://arxiv.org/pdf/1811.12926.pdf Appendix A. The latter goes through a
    7-step process involving various decompositions, routing, and optimization
    steps. We route the model circuit and then run a series of optimizers on it
    (which can be passed into this function).

    Args:
        circuit: The model circuit to compile.
        device: The device to compile onto.
        compiler: An optional function to deconstruct the model circuit's
            gates down to the target devices gate set and then optimize it.

    Returns: A tuple where the first value is the compiled circuit and the
        second value is the final mapping from the model circuit to the compiled
        circuit. The latter is necessary in order to preserve the measurement
        order.

    """
    compiled_circuit = circuit.copy()
    # Swap Mapping (Routing). Ensure the gates can actually operate on the
    # target qubits given our topology.
    if router is None and routing_algo_name is None:
        routing_algo_name = 'greedy'
    swap_network = ccr.route_circuit(compiled_circuit,
                                     ccr.xmon_device_to_graph(device),
                                     router=router,
                                     algo_name=routing_algo_name)
    compiled_circuit = swap_network.circuit

    # Compile. This should decompose the routed circuit down to a gate set that
    # our device supports, and then optimize. The paper uses various
    # compiling techniques - because Quantum Volume is intended to test those
    # as well, we allow this to be passed in. This compiler is not allowed to
    # change the order of the qubits.
    if compiler:
        compiled_circuit = compiler(compiled_circuit)

    return compiled_circuit, swap_network.final_mapping()


@dataclass
class QuantumVolumeResult:
    """Stores one run of the results and test information used when running the
    quantum volume benchmark so it may be analyzed in detail afterwards.

    """
    # The model circuit used.
    model_circuit: cirq.Circuit
    # The heavy set computed from the above model circuit.
    heavy_set: List[int]
    # The mdel circuit after being compiled.
    compiled_circuit: cirq.Circuit
    # The sampler's list of probabilities.
    sampler_result: List[float]

    def _json_dict_(self):
        return cirq.protocols.obj_to_dict_helper(self, [
            'model_circuit', 'heavy_set', 'compiled_circuit', 'sampler_result'
        ])


def prepare_circuits(
        *,
        num_qubits: int,
        depth: int,
        num_repetitions: int,
        random_state: Optional[np.random.RandomState] = None,
) -> List[Tuple[cirq.Circuit, List[int]]]:
    """Generates circuits and computes their heavy set.

    Args:
        num_qubits: The number of qubits in the generated circuits.
        depth: The number of layers in the circuits.
        num_repetitions: The number of circuits to create.
        random_state: A way to seed the RandomState.

    Returns:
        A list of tuples where the first element is a generated model
        circuit and the second element is the heavy set for that circuit.
    """
    circuits = []
    for repetition in range(num_repetitions):
        model_circuit = generate_model_circuit(num_qubits,
                                               depth,
                                               random_state=random_state)
        heavy_set = compute_heavy_set(model_circuit)
        print(f"Repetition {repetition + 1} Heavy Set: {heavy_set}")
        circuits.append((model_circuit, heavy_set))
    return circuits


def execute_circuits(*,
                     device: cirq.google.xmon_device.XmonDevice,
                     samplers: List[cirq.Sampler],
                     compiler: Callable[[cirq.Circuit], cirq.Circuit] = None,
                     circuits: List[Tuple[cirq.Circuit, List[int]]]
                    ) -> List[QuantumVolumeResult]:
    """Executes the given circuits on the given samplers.

    Args
        device: The device to run the compiled circuit on.
        samplers: The samplers to run the algorithm on.
        compiler: An optional function to compiler the model circuit's
            gates down to the target devices gate set and the optimize it.
        circuits: The circuits to sample from.

    Returns:
        A list of QuantumVolumeResults that contains all of the information for
        running the algorithm and its results.

    """
    results = []
    for model_circuit, heavy_set in circuits:
        compiled_circuit, mapping = compile_circuit(model_circuit,
                                                    device=device,
                                                    compiler=compiler)
        sampler_result = []
        for idx, sampler in enumerate(samplers):
            prob = sample_heavy_set(compiled_circuit,
                                    heavy_set,
                                    sampler=sampler,
                                    mapping=mapping)
            print(f"  Compiled HOG probability #{idx + 1}: {prob}")
            sampler_result.append(prob)
            results.append(
                QuantumVolumeResult(model_circuit=model_circuit,
                                    heavy_set=heavy_set,
                                    compiled_circuit=compiled_circuit,
                                    sampler_result=sampler_result))
    return results


def calculate_quantum_volume(
        *,
        num_qubits: int,
        depth: int,
        num_repetitions: int,
        seed: int,
        device: cirq.google.xmon_device.XmonDevice,
        samplers: List[cirq.Sampler],
        compiler: Callable[[cirq.Circuit], cirq.Circuit] = None,
) -> List[QuantumVolumeResult]:
    """Run the quantum volume algorithm.

    This algorithm should compute the same values as Algorithm 1 in
    https://arxiv.org/abs/1811.12926. To summarize, we generate a random model
    circuit, compute its heavy set, then transpile an implementation onto our
    architecture. This implementation is run a series of times and if the
    percentage of outputs that are in the heavy set is greater than 2/3, we
    consider the quantum volume test passed for that size.

    Args:
        num_qubits: The number of qubits for the circuit.
        depth: The number of gate layers to generate.
        num_repetitions: The number of times to run the algorithm.
        seed: A seed to pass into the RandomState.
        device: The device to run the compiled circuit on.
        samplers: The samplers to run the algorithm on.
        compiler: An optional function to compiler the model circuit's
            gates down to the target devices gate set and the optimize it.

    Returns: A list of QuantumVolumeResults that contains all of the information
        for running the algorithm and its results.

    """
    random_state = np.random.RandomState(seed)
    circuits = prepare_circuits(num_qubits=num_qubits,
                                depth=depth,
                                num_repetitions=num_repetitions,
                                random_state=random_state)
    return execute_circuits(circuits=circuits,
                            device=device,
                            compiler=compiler,
                            samplers=samplers)
