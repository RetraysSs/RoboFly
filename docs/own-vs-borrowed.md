# Written by me vs. used as-is

Rule: if a part carries the project's claim or my learning goal, I write it. If it is solved, infrastructure, or data only a large team could produce, I use it. Where possible I write my own version first and then validate it against the established one.

## Written by me

| Part | Validated against |
|---|---|
| LIF neuron and network simulator | Brian2 (v0.2) |
| Connectome loader and sparse weight matrix | Published model repos (counts, known pathways) |
| Sensor to neuron encoder, neuron to motor decoder | n/a (project-specific) |
| Ridge regression readout | scikit-learn |
| Reward-based readout update | Offline ridge solution |
| Virtual 2D world | n/a |
| Serial protocol, CRC, framing | Unit tests, fault injection |
| STM32 control loop, ADC/PWM logic | Logic analyser / scope measurements |
| Experiments and analysis scripts | n/a |

## Used as-is

| Part | Why |
|---|---|
| FlyWire connectome and annotations | Years of work by hundreds of people |
| Brian2 | Reference simulator for validation only |
| NumPy, SciPy, Matplotlib, pySerial, pytest | Standard tools |
| STM32 HAL / CubeMX clock setup, USB CDC stack | Solved infrastructure; application logic is mine |
| Motor driver and sensor modules | Hardware |

## Read, not copied

The Shiu et al. model code and the Eon Systems fly-brain repo are read to understand the method. Code is not pasted into this repository; if an idea is borrowed it is credited in the relevant dev log entry.

## Possible extensions

- Replace HAL calls in the firmware with direct register access for one peripheral.
- Write a CRC-16 table-driven and bitwise version and compare speed on the MCU.
