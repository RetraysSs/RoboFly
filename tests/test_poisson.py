"""Tests for the Poisson spike generator (task v0.2-03).

Skipped until src/flybot/inputs.py exists.
"""
import numpy as np
import pytest

inputs = pytest.importorskip("flybot.inputs")
poisson_spikes = inputs.poisson_spikes

DT = 0.1  # ms


def test_shape_and_dtype():
    s = poisson_spikes(50.0, 1000, DT, n=3, rng=np.random.default_rng(0))
    assert s.shape == (1000, 3)
    assert s.dtype == bool


def test_zero_rate_gives_no_spikes():
    s = poisson_spikes(0.0, 5000, DT, n=2, rng=np.random.default_rng(0))
    assert not s.any()


def test_same_seed_gives_same_spikes():
    a = poisson_spikes(80.0, 5000, DT, n=2, rng=np.random.default_rng(42))
    b = poisson_spikes(80.0, 5000, DT, n=2, rng=np.random.default_rng(42))
    np.testing.assert_array_equal(a, b)


def test_mean_rate():
    steps = 200_000  # 20 s
    s = poisson_spikes(100.0, steps, DT, n=1, rng=np.random.default_rng(1))
    rate = s.sum() / (steps * DT / 1000.0)
    assert rate == pytest.approx(100.0, rel=0.10)


def test_rate_can_differ_per_neuron():
    steps = 200_000
    s = poisson_spikes(np.array([0.0, 200.0]), steps, DT, n=2,
                       rng=np.random.default_rng(2))
    assert s[:, 0].sum() == 0
    rate = s[:, 1].sum() / (steps * DT / 1000.0)
    assert rate == pytest.approx(200.0, rel=0.10)


def test_counts_are_poisson_like():
    # For a Poisson process the variance of spike counts in fixed windows equals
    # their mean (Fano factor close to 1).
    steps = 1_000_000  # 100 s
    s = poisson_spikes(50.0, steps, DT, n=1, rng=np.random.default_rng(3))[:, 0]
    counts = s.reshape(-1, 1000).sum(axis=1)  # 100 ms windows
    fano = counts.var() / counts.mean()
    assert 0.8 < fano < 1.2


def test_rate_too_high_for_time_step_raises():
    # 20 000 Hz at dt = 0.1 ms would need 2 spikes per step.
    with pytest.raises(ValueError):
        poisson_spikes(20_000.0, 100, DT)
