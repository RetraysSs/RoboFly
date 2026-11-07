# Architecture

Working document. Numbers marked **TBD** are measured in the version named next to them.

## Data flow (one control cycle)

1. **Robot:** sample sensors (ADC + DMA), timestamp, build packet, send to PC.
2. **PC encoder:** map each sensor value to a stimulation rate (Hz) for a chosen group of sensory neurons.
3. **PC simulator:** advance the connectome LIF simulation by one window (a few tens to ~200 ms of simulated time, **TBD v0.3/v0.7**) with that stimulation.
4. **PC decoder:** compute firing rates of chosen output neurons over the window; the learned linear readout turns them into a motor command (left/right wheel speeds).
5. **Robot:** receive command, validate (CRC, sequence number, age), apply to PWM. If no valid command arrives within a timeout, **stop the motors**.

## Why the brain runs on the PC

The full connectome has about 139,000 neurons and 50 million synapses. A GPU (RTX 4060) can plausibly run it; an MCU cannot. The robot keeps the hard-real-time parts (sampling, PWM, safety), the PC keeps the heavy simulation. Whether the full network keeps up with the control loop is measured in v0.3; the fallback is a documented subcircuit.

## Components

| Component | Language | Version | Notes |
|---|---|---|---|
| LIF simulator | Python (NumPy, later GPU) | v0.1-v0.3 | Written from scratch, validated against Brian2 |
| Encoder / decoder | Python | v0.4 | Neuron sets chosen from FlyWire annotations |
| Readout learning | Python | v0.5 | Ridge regression, then reward-based updates |
| Virtual world | Python | v0.5 | Point agent, light source, noisy sensor |
| Firmware | C (STM32F407, HAL) | v0.6 | ADC+DMA, PWM, timer-driven loop, USB CDC |
| Host bridge | Python (pySerial) | v0.6 | Protocol, logging, latency measurement |

## Serial protocol (sketch, to be finalised in v0.6)

```
| SOF | LEN | TYPE | SEQ | PAYLOAD ... | CRC16 |
```

- `SOF`: start-of-frame marker for resynchronisation.
- `LEN`: payload length.
- `TYPE`: sensor report / motor command / heartbeat / error.
- `SEQ`: sequence number to detect drops and measure latency.
- `CRC16`: integrity check over header and payload.

To be written up in `docs/protocol.md` when v0.6 starts.

## Timing budget (to be measured)

| Stage | Budget | Measured |
|---|---|---|
| Sensor sample + packet | TBD | v0.6 |
| Serial transfer | TBD | v0.6 |
| Encode + simulate window | TBD | v0.3 / v0.7 |
| Decode + readout | TBD | v0.5 |
| Serial transfer + PWM update | TBD | v0.6 |
| **Control period** | TBD | v0.7 |

## Hardware

- PC with NVIDIA RTX 4060 (simulation).
- STM32F407G-DISC1 (robot controller, v0.6 onward).
- Arduino UNO Q 4GB (possible wireless/standalone bridge, after v1.0).
- Chassis, two motors, motor driver, light sensors, optional distance sensor (to buy when v0.4 passes its decision gate).
