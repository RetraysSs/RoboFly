import numpy as np

def simulate_lif(
    i_ext,            # 1-D array, input current in nA, one value per time step
    dt,                        # time step in ms
    *,
    tau_m=20.0,       # ms
    v_rest=-70.0,     # mV
    v_reset=-75.0,    # mV
    v_th=-50.0,       # mV
    r_m=10.0,         # MOhm
    t_ref=0.0,        # ms, refractory period (0 = none)
):
    """Return (v, spike_times).

    v: array, same length as i_ext, membrane potential at each step
    spike_times: array of spike times in ms

    Conventions:
    - v[0] = v_rest.
    - A spike is recorded at time (step + 1) * dt, when the new potential
      reaches v_th.
    - On a spike step the stored v is v_reset, not the pre-reset peak.
    """

    n = len(i_ext)
    v = np.zeros(n)
    spikes = []
    v[0] = v_rest
    counter = 0

    for step in range(n-1):
        v[step + 1] = v[step] + dt / tau_m * (-(v[step] - v_rest) + r_m * i_ext[step])
        if counter > 0:
            counter = counter - 1
            v[step + 1] = v_reset
            continue
        if v_th <= v[step + 1]:
            time = dt * (step + 1)
            spikes.append(time)
            v[step + 1] = v_reset
            counter = round((t_ref / dt))




    return v,np.array(spikes)


