# connectome-robot

A small wheeled robot whose "brain" is the **real wiring diagram of an adult fruit fly** (the FlyWire connectome), run as a spiking-neuron simulation on a PC. A microcontroller (STM32F407) does the real-time sensing and motor control and talks to the simulation over a custom protocol. A small learned readout layer lets the robot adapt over time while the connectome itself stays fixed.

> **Status:** `v0.1` in progress. See [ROADMAP.md](ROADMAP.md) for what each version builds and what to study for it.

## What this project is (and is not)

**Is:** a hands-on embedded + software project. Real biological wiring data drives a real robot through a closed loop: sensor -> neuron stimulation -> simulated spiking activity -> motor command -> motion -> sensor.

**Is not:**
- Not an "uploaded fly". A connectome is a static wiring diagram of one fly's brain, not a living brain. It does not contain synaptic strengths in the physical sense, neuromodulation state, or learning rules.
- Not the full fly behaviour repertoire. The robot will implement one or two simple reflex-like behaviours (for example, approaching a light), selected from the circuit's input and output neurons.
- Not a claim that the simulated circuit "causes" the behaviour the way it does in a real fly. The neuron model is deliberately simple (leaky integrate-and-fire).

These limits are part of the project. Every version records what worked and what did not, including negative results.

## Architecture

```
   ROBOT (STM32F407, C)                       PC (RTX 4060, Python)
 +-----------------------+   USB serial   +------------------------------+
 | light/distance sensors|  -- sensors -> | encode: sensor -> stimulation|
 | ADC + DMA             |                |   of chosen sensory neurons  |
 |                       |                |            |                 |
 | fixed-period control  |                |  FlyWire connectome (fixed)  |
 | loop, CRC protocol    |                |  LIF spiking simulation      |
 |                       |                |            |                 |
 | PWM motor drive       | <- commands -- | decode: output-neuron rates  |
 +-----------------------+                |  -> learned linear readout   |
                                          |  -> motor command            |
                                          +------------------------------+
```

The connectome is **fixed**. Learning happens only in a small linear readout layer (reservoir-computing style) and, optionally, in the input encoding. Changing synapses inside the connectome itself is a possible future version, not part of v1.0.

More detail: [docs/architecture.md](docs/architecture.md).

## Roadmap at a glance

| Version | Focus | Deliverable |
|---|---|---|
| v0.1 | Foundations, own single-neuron LIF | Plotted membrane trace, passing tests |
| v0.2 | Own LIF network simulator, checked against Brian2 | Matching spike rasters |
| v0.3 | Load the FlyWire connectome, run it, benchmark it | Raster plots, speed table |
| v0.4 | Choose input/output neurons, measure responses (**decision gate**) | Response-curve notebook |
| v0.5 | Virtual closed loop and learned readout | Learning curve in simulation |
| v0.6 | STM32 firmware and host bridge | Robot driven from PC, latency numbers |
| v0.7 | Hardware-in-the-loop integration | First real closed-loop run |
| v0.8 | Learning on the real robot, control experiments | Connectome vs random-network comparison |
| v1.0 | Write-up and release | Video, report, limitations |

Details, study material and acceptance criteria for each version are in [ROADMAP.md](ROADMAP.md).

## Repository layout

```
src/flybot/        Python package: simulator, encoders/decoders, learning
tests/             Automated tests
tasks/             Step-by-step task specs for the current version
experiments/       Reproducible experiment scripts and notebooks
host/              PC-side robot bridge (serial protocol, logging)
firmware/stm32f407 Robot firmware in C
data/              Connectome files (not committed, see data/README.md)
docs/              Architecture, glossary, own-vs-borrowed, dev log
```

## Written by me vs. used as-is

This project is meant to demonstrate understanding, so the split is explicit. See [docs/own-vs-borrowed.md](docs/own-vs-borrowed.md).

In short: the LIF simulator, the sensor/neuron encoding, the readout learning, the serial protocol and the firmware are written from scratch. The connectome data, Brian2 (used only as a reference to validate my simulator), NumPy/SciPy and the STM32 HAL/USB stack are used as-is.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
pytest
```

Optional extras: `pip install -e ".[ref]"` installs Brian2 for validation work (v0.2 onward), `pip install -e ".[robot]"` installs pySerial for the host bridge (v0.6 onward).

## Credits and citations

This project builds on public research data and models. If you use anything here, please cite the originals:

- Dorkenwald et al., *Neuronal wiring diagram of an adult brain*, Nature 634, 124-138 (2024). doi:10.1038/s41586-024-07558-y
- Schlegel et al., *Whole-brain annotation and multi-connectome cell typing of Drosophila*, Nature 634, 139-152 (2024). doi:10.1038/s41586-024-07686-5
- Shiu et al., *A Drosophila computational brain model reveals sensorimotor processing*, Nature 634, 210-219 (2024). doi:10.1038/s41586-024-07763-9
- FlyWire Codex: https://codex.flywire.ai/

Connectome data is **not** redistributed in this repository. See [data/README.md](data/README.md).
