import numpy as np
import matplotlib.pyplot as plt
from flybot.lif import simulate_lif
from pathlib import Path

dt = 0.1
currents = [1.0, 2.0, 3.0, 4.0]

fig, axes = plt.subplots(4, 1, sharex=True)  # 4 row and 1 col

for ax,c in zip(axes, currents):
    i_ext= np.full(5000,c)
    v,spikes = simulate_lif(i_ext,dt)
    t = np.arange(len(v)) * dt
    ax.set_title(f"{c} nA")
    ax.plot(spikes, [-50] * len(spikes), "r.")
    ax.plot(t,v)



axes[-1].set_xlabel("Time (ms)")
fig.supylabel("Membrane potential (mV)")
out_dir = Path(__file__).resolve().parent.parent / "docs" / "figures"
out_dir.mkdir(parents=True, exist_ok=True)
plt.savefig(out_dir / "v0_1_single_neuron.png", dpi=150)
plt.show()
