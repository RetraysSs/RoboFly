"""Tests for the LIF network without synapses (task v0.2-01).

Skipped until src/flybot/network.py exists. The tests check properties of the
model and compare the network against the single-neuron simulator from v0.1.
"""
import numpy as np
import pytest

network = pytest.importorskip("flybot.network")
lif = pytest.importorskip("flybot.lif")
LIFNetwork = network.LIFNetwork
simulate_lif = lif.simulate_lif

DT = 0.1  # ms
V_REST = -70.0


def make(n, **kwargs):
    return LIFNetwork(np.zeros((n, n)), DT, **kwargs)


def test_initial_state():
    net = make(4)
    assert net.n == 4
    assert net.v.shape == (4,)
    assert np.allclose(net.v, V_REST)
    assert net.t == 0.0


def test_step_returns_boolean_mask_and_advances_time():
    net = make(3)
    spiked = net.step(0.0)
    assert spiked.dtype == bool
    assert spiked.shape == (3,)
    assert not spiked.any()
    assert net.t == pytest.approx(DT)


def test_run_output_format():
    steps = 3000
    net = make(3)
    times, ids = net.run(np.full((steps, 3), 3.0))
    assert len(times) == len(ids) > 0
    assert np.all(np.diff(times) >= 0), "spike times must be sorted"
    assert ids.min() >= 0 and ids.max() < 3
    assert times.max() <= steps * DT + 1e-9


def test_1d_current_is_applied_to_all_neurons():
    net = make(3)
    _, ids = net.run(np.full(4000, 3.0))
    counts = np.bincount(ids, minlength=3)
    assert counts[0] == counts[1] == counts[2] > 0


def test_independent_neurons_match_single_neuron_simulation():
    currents = [0.0, 3.0, 4.0]
    steps = 4000
    net = make(3)
    times, ids = net.run(np.tile(np.array(currents), (steps, 1)))
    for j, c in enumerate(currents):
        # run() performs len(i_ext) updates, simulate_lif performs len(i_ext) - 1,
        # so one extra sample is appended for the single-neuron reference.
        _, ref = simulate_lif(np.append(np.full(steps, c), 0.0), DT)
        np.testing.assert_allclose(times[ids == j], ref, atol=1e-9)


def test_refractory_matches_single_neuron_simulation():
    steps = 3000
    net = make(1, t_ref=10.0)
    times, _ = net.run(np.full((steps, 1), 10.0))
    _, ref = simulate_lif(np.append(np.full(steps, 10.0), 0.0), DT, t_ref=10.0)
    np.testing.assert_allclose(times, ref, atol=1e-9)
    assert np.min(np.diff(times)) >= 10.0 - 1e-9


def test_state_persists_across_runs():
    # A closed-loop robot calls run() repeatedly on short windows, so splitting
    # one long run into two calls must give the same result.
    rng = np.random.default_rng(0)
    i_ext = rng.uniform(0.0, 4.0, size=(3000, 5))
    whole = make(5)
    t_all, id_all = whole.run(i_ext)
    split = make(5)
    t1, id1 = split.run(i_ext[:1234])
    t2, id2 = split.run(i_ext[1234:])
    np.testing.assert_allclose(np.concatenate([t1, t2]), t_all, atol=1e-9)
    np.testing.assert_array_equal(np.concatenate([id1, id2]), id_all)


def test_unconnected_neurons_do_not_interact():
    net = make(2)
    i_ext = np.zeros((3000, 2))
    i_ext[:, 0] = 4.0
    _, ids = net.run(i_ext)
    assert len(ids) > 0
    assert np.all(ids == 0)
