"""Tests for the single LIF neuron (task v0.1-01).

They are skipped until src/flybot/lif.py exists. They check physical properties
of the model rather than comparing against one specific implementation.
"""
import numpy as np
import pytest

lif = pytest.importorskip("flybot.lif")
simulate_lif = lif.simulate_lif

DT = 0.1  # ms
T_STEPS = 5000  # 500 ms

# Default parameters used by the tests (must match the defaults in the spec).
TAU_M, V_REST, V_RESET, V_TH, R_M = 20.0, -70.0, -75.0, -50.0, 10.0


def run(i_na, steps=T_STEPS, dt=DT, **kwargs):
    i_ext = np.full(steps, float(i_na))
    return simulate_lif(i_ext, dt, **kwargs)


def test_output_shapes():
    v, spikes = run(3.0)
    assert len(v) == T_STEPS
    assert np.ndim(spikes) == 1


def test_no_input_stays_at_rest():
    v, spikes = run(0.0)
    assert len(spikes) == 0
    assert np.allclose(v, V_REST, atol=1e-6)


def test_subthreshold_input_converges_without_spiking():
    # 1 nA * 10 MOhm = 10 mV, so the steady state is -60 mV, below threshold.
    v, spikes = run(1.0)
    assert len(spikes) == 0
    assert v[-1] == pytest.approx(V_REST + R_M * 1.0, abs=0.05)


def test_suprathreshold_input_spikes_regularly():
    # With 3 nA the interval between spikes follows from the closed-form
    # solution of the LIF equation (no refractory period).
    i = 3.0
    drive = R_M * i  # 30 mV above rest
    isi_expected = TAU_M * np.log((drive - (V_RESET - V_REST)) / (drive - (V_TH - V_REST)))
    _, spikes = run(i)
    assert len(spikes) >= 5
    isi = np.diff(spikes)
    assert np.mean(isi) == pytest.approx(isi_expected, rel=0.05)
    # Regular firing: intervals nearly constant after the first spike.
    assert np.std(isi) < 0.05 * np.mean(isi) + DT


def test_firing_rate_increases_with_input():
    _, low = run(3.0)
    _, high = run(4.0)
    assert len(high) > len(low) > 0


def test_spike_times_inside_simulation_window():
    _, spikes = run(3.0)
    assert np.all(spikes >= 0.0)
    assert np.all(spikes <= T_STEPS * DT)


def test_membrane_potential_never_exceeds_threshold_after_reset():
    # The stored potential may show the pre-reset peak (documented choice), but
    # it must never run far past threshold: a large overshoot means a bug.
    v, _ = run(4.0)
    assert np.max(v) < V_TH + 5.0


def test_refractory_period_limits_rate():
    t_ref = 5.0
    _, spikes = run(10.0, t_ref=t_ref)  # very strong drive
    assert len(spikes) >= 5
    assert np.min(np.diff(spikes)) >= t_ref - 1e-9
