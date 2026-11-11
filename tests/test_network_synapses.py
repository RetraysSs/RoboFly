"""Tests for synapses, mutable weights and the step hook (task v0.2-02).

Convention under test: weights[i, j] is the voltage jump in mV that neuron i
receives when neuron j spikes. The jump is added at the end of the step in which
the spike occurred, so a postsynaptic spike can appear at the earliest one step
later.
"""
import numpy as np
import pytest

network = pytest.importorskip("flybot.network")
LIFNetwork = network.LIFNetwork

DT = 0.1  # ms
TAU_M = 20.0
V_REST = -70.0


def pair(w):
    weights = np.zeros((2, 2))
    weights[1, 0] = w  # neuron 0 -> neuron 1
    return LIFNetwork(weights, DT)


def drive_until_spike(net, neuron, current, max_steps=5000):
    i_ext = np.zeros(net.n)
    i_ext[neuron] = current
    for _ in range(max_steps):
        spiked = net.step(i_ext)
        if spiked[neuron]:
            return
    raise AssertionError("neuron never spiked")


def test_excitatory_jump_and_leak():
    w = 5.0
    net = pair(w)
    drive_until_spike(net, 0, 3.0)
    assert net.v[1] == pytest.approx(V_REST + w)
    net.step(np.zeros(2))
    assert net.v[1] == pytest.approx(V_REST + w * (1 - DT / TAU_M))


def test_inhibitory_jump():
    net = pair(-5.0)
    drive_until_spike(net, 0, 3.0)
    assert net.v[1] == pytest.approx(V_REST - 5.0)


def test_postsynaptic_spike_follows_one_step_later():
    net = pair(25.0)  # strong enough to push neuron 1 over threshold
    times, ids = net.run(np.tile([3.0, 0.0], (3000, 1)))
    t0 = times[ids == 0][0]
    t1 = times[ids == 1][0]
    assert t1 == pytest.approx(t0 + DT)


def test_spikes_propagate_along_a_chain():
    weights = np.zeros((3, 3))
    weights[1, 0] = 25.0
    weights[2, 1] = 25.0
    net = LIFNetwork(weights, DT)
    times, ids = net.run(np.tile([3.0, 0.0, 0.0], (3000, 1)))
    t0, t1, t2 = (times[ids == k][0] for k in range(3))
    assert t1 == pytest.approx(t0 + DT)
    assert t2 == pytest.approx(t1 + DT)


def test_inhibition_reduces_firing():
    i_ext = np.tile([4.0, 2.5], (5000, 1))
    free = pair(0.0)
    _, ids_free = free.run(i_ext)
    inhibited = pair(-3.0)
    _, ids_inh = inhibited.run(i_ext)
    assert np.sum(ids_inh == 1) < np.sum(ids_free == 1)
    assert np.sum(ids_free == 1) > 0


def test_sparse_weights_match_dense():
    sparse = pytest.importorskip("scipy.sparse")
    rng = np.random.default_rng(1)
    n = 50
    # Weights are multiples of 0.5 so the sums are exact in floating point and
    # the dense and sparse products agree bit for bit.
    dense = rng.integers(-6, 7, size=(n, n)) * 0.5 * (rng.random((n, n)) < 0.1)
    i_ext = rng.uniform(2.0, 3.5, size=(2000, n))
    t_d, id_d = LIFNetwork(dense, DT).run(i_ext)
    t_s, id_s = LIFNetwork(sparse.csr_matrix(dense), DT).run(i_ext)
    assert len(t_d) > 0
    np.testing.assert_allclose(t_s, t_d, atol=1e-9)
    np.testing.assert_array_equal(id_s, id_d)


def test_weights_are_mutable_state():
    net = pair(0.0)
    i_ext = np.tile([3.0, 0.0], (2000, 1))
    _, ids = net.run(i_ext)
    assert not np.any(ids == 1)
    net.weights[1, 0] = 25.0  # change a single weight in place
    _, ids = net.run(i_ext)
    assert np.any(ids == 1)


def test_weights_can_be_replaced():
    sparse = pytest.importorskip("scipy.sparse")
    net = pair(0.0)
    i_ext = np.tile([3.0, 0.0], (2000, 1))
    new = np.zeros((2, 2))
    new[1, 0] = 25.0
    net.weights = sparse.csr_matrix(new)
    _, ids = net.run(i_ext)
    assert np.any(ids == 1)


def test_on_step_hook():
    net = pair(0.0)
    steps = 2000
    calls = []

    def hook(network_, k, spiked):
        calls.append((k, spiked.copy()))
        if k == 500:
            network_.weights[1, 0] = 25.0

    times, ids = net.run(np.tile([3.0, 0.0], (steps, 1)), on_step=hook)
    assert [c[0] for c in calls] == list(range(steps))
    assert all(c[1].dtype == bool and c[1].shape == (2,) for c in calls)
    # Neuron 1 is silent until the hook changes the weight after step 500.
    assert np.any(ids == 1)
    assert times[ids == 1].min() > 500 * DT


def test_refractory_neuron_ignores_external_jumps():
    net = LIFNetwork(np.zeros((1, 1)), DT, t_ref=10.0)
    steps = 3000
    jumps = np.full((steps, 1), 30.0)  # large kick on every step
    times, _ = net.run(np.zeros((steps, 1)), jump_ext=jumps)
    assert len(times) >= 5
    assert np.min(np.diff(times)) >= 10.0 - 1e-9
