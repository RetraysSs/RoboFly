# Firmware: STM32F407G-DISC1

Starts in **v0.6**. Planned contents:

- STM32CubeIDE or CMake project (HAL for clock setup and USB CDC; application logic written by me).
- ADC + DMA sensor sampling.
- PWM motor output.
- Timer-driven fixed-period control loop.
- Packet protocol with CRC (see `docs/architecture.md` and, later, `docs/protocol.md`).
- Safe stop on link loss.

Do not start here before v0.4 has passed its decision gate unless you want a break from simulation work; the firmware track is independent of the simulator until v0.7.
