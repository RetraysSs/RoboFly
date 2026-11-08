# Firmware: STM32F407G-DISC1

Starts in **v0.6**. Planned contents:

- STM32CubeIDE or CMake project (HAL for clock setup and USB CDC; application logic written by me).
- ADC + DMA sensor sampling.
- PWM motor output.
- Timer-driven fixed-period control loop.
- Packet protocol with CRC (see `docs/architecture.md` and, later, `docs/protocol.md`).
- Safe stop on link loss.

The firmware track is independent of the simulator until v0.7 and can run in parallel with v0.3-v0.5. Hardware purchases wait for the v0.4 decision gate.
