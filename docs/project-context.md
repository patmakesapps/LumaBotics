# LumaBot Project Context

Updated July 14, 2026.

## Goal

Build a small entertainment-focused differential-drive desk companion that:

- drives with two independently controlled wheels;
- avoids obstacles;
- supports microphone and speaker voice interaction;
- uses a forward-facing Pi NoIR camera;
- eventually has a servo-driven tilt head;
- connects to the LumaKit agent framework; and
- uses cloud LLM APIs over Wi-Fi rather than a local LLM.

The prototype must require no soldering.

## Repositories and Hosts

- Robot: <https://github.com/patmakesapps/LumaBotics>
- Windows checkout: `C:\LumaBot`
- Agent framework: <https://github.com/patmakesapps/LumaKit>
- LumaKit is updated and installed on the Pi 5 in Pat's home folder.
- LumaKit integration is deferred until the physical robot works.

## Current Codebase

- `brain.py`: hardware-independent, reactive, pose-blind three-state controller
  (`cruise`, `backup`, and `turn`). It uses non-blocking deadlines, emits
  normalized left/right speeds from -1 to 1, and randomizes turn direction and
  duration.
- `robot.py`: real 20 Hz sense-decide-act loop using `time.monotonic()`.
  `read_sensor()` and `set_motors()` are the unimplemented hardware seams.
- `simulation/sim.py`: Turtle simulation with differential-drive physics,
  furniture, walls, and a U-shaped trap.
- `simulation/sensor.py`: ray-cast simulated distance sensor with self-tests.
- `docs/notes.txt`: simulation tuning notes.

Completed learning chunks: differential-drive physics, ray-cast sensing, the
brain/state machine and full simulation, simulation/hardware separation, and
Git repository setup/refactoring.

## Hardware

Already owned:

- Raspberry Pi 5, Pi NoIR camera, and Pi 5-compatible 22-pin camera ribbon.
- Pi fans/heatsinks, USB-C supply, and microSD card.
- Pi configured on the network.

Ordered:

- Three Acxico N20 3-6 V gear motors with wired leads, 3 mm D-shafts, and
  approximately 104 RPM. Use two; keep one spare.
- 65 mm K346 rubber wheels with 3 mm D-holes, expected July 28-August 4.
- MECCANIXITY N20 brackets with screws.
- Four MARRTEUM ball-bearing casters. Use one rear caster; keep three spares.
- Waveshare PCA9685 + TB6612FNG I2C Motor Driver HAT with two DC outputs.
- Pi 5 WM8960 Audio HAT with dual MEMS microphones and two included 8 ohm,
  5 W speakers. The HAT supplies approximately 1 W per channel.
- CQRobot VL53L1X time-of-flight sensor.
- Geekworm X1200 UPS HAT and two Samsung 35E flat-top unprotected 18650 cells.
- Extra-tall 2x20 stacking headers and female-to-female/male-to-female Dupont
  jumpers.
- Four SG90 servos.
- 4xAA 6 V battery holders with covers, bare leads, and switches.
- Four alkaline AA cells are required for motor testing.

Do not suggest additional purchases until testing demonstrates a need.

## Electrical Architecture

### X1200

- Mount below the Pi using pogo pins.
- The two 18650 cells are parallel, not a 7.4 V series pack.
- It supplies approximately 5.1 V/5 A to the Pi.
- Power and charge only through the X1200 USB-C port.
- Never power the Pi USB-C port while the X1200 is installed.
- Expected battery-gauge I2C address: `0x36`.

### Motor Driver HAT

- Mount separately on the chassis; do not stack it on the Pi.
- Official VIN range is 6-12 V. For the prototype, use four alkaline AA cells
  in series for 6 V.
- Battery red connects to VIN positive. Battery black connects to VIN
  negative/GND.
- Connect the Pi to the powered HAT using only GND, SDA, and SCL.
- Never connect the Motor HAT 5 V pin to the Pi. Its regulator could backfeed
  the independently powered Pi/X1200.
- Channel A drives the left motor; channel B drives the right motor.
- Verify the PCA9685 IN1/IN2 channel mapping from the physical board and
  official example before implementing it.
- Correct reversed wheels with software inversion flags instead of repeatedly
  changing motor wiring.
- No servo channels are exposed, so motor PWM can run independently, potentially
  near 1 kHz.

### Servo

- Drive the SG90 signal from an unused Pi GPIO.
- Do not use GPIO18-GPIO21; the WM8960 uses them for I2S.
- Servo red connects to regulated 5 V, brown to ground, and orange/yellow to the
  selected GPIO signal.
- All power-system grounds must be common.
- The Motor HAT 5 V output may power the servo from the AA pack, but verify the
  physical header before wiring.
- Male-to-female jumpers can break the SG90 female connector into separate
  signal, power, and ground connections.

### Expected I2C Addresses

- `0x1A`: WM8960 audio codec.
- `0x29`: VL53L1X sensor.
- `0x36`: X1200 battery gauge.
- `0x40`: Motor HAT PCA9685.
- `0x70`: possible PCA9685 all-call address.

I2C fan-out remains a physical question. Inspect whether the extra-tall header
leaves usable pins around or above the WM8960. Do not buy a splitter
preemptively. Removing the audio HAT during initial driving tests is acceptable.

## Mechanical Architecture

- Use two driven wheels and one rear caster. Three contact points prevent
  rocking and keep both drive wheels loaded; do not install all four casters.
- Wait for the actual motors, brackets, wheels, caster, and electronics before
  finalizing mounting holes.
- First print a simple functional flat chassis, approximately 140 x 110 mm,
  before designing the polished shell.
- Add adjustable/slotted bracket holes, zip-tie slots, ventilation, and one
  X1200 USB-C charging cutout.
- Keep the batteries and heavy electronics low and centered.
- Do not purchase a generic robot chassis.
- Fix the camera forward for v1 at approximately 10-15 degrees downward.
- Install the camera ribbon before the audio HAT obstructs access.
- Later add tilt only. Avoid pan because repeated ribbon twisting is undesirable.

## Bring-Up Order

1. Verify Raspberry Pi OS, kernel, SSH, and I2C. Record `uname -a`. Test the
   camera before installing HATs.
2. Install the X1200 below the Pi, carefully seat its pogo pins, insert correctly
   oriented cells, power through X1200 USB-C, confirm a stable boot, and look for
   I2C address `0x36`.
3. Check fan/heatsink and WM8960 clearance. Install the audio HAT with the tall
   header, look for `0x1A`, install the kernel-appropriate driver, then test
   speakers, microphones, and first TTS output.
4. Connect the VL53L1X, remove its protective film, look for `0x29`, and
   implement `read_sensor()` as a small guided chunk.
5. Connect Motor HAT GND/SDA/SCL with motors and AA power disconnected. Verify
   I2C detection.
6. Connect the AA holder to VIN without connecting HAT 5 V to the Pi. Keep
   wheels off the ground, test one motor at a time, verify channel mapping,
   direction, and emergency stop behavior, then implement `set_motors()` as a
   small guided chunk.
7. Connect and test one SG90 using GPIO signal, regulated 5 V, and common ground.
8. Print the measured basic chassis and test driving, turning, and avoidance.
9. Wrap proven speak/listen/move/measure capabilities as LumaKit agent tools.

The immediate next stage is the main hardware delivery around July 19, followed
by audio/X1200/camera bring-up one component at a time. Wheels arrive later, so
motor bench testing can happen first. Always resume from Pat's reported state.

## Known Gotchas

- The WM8960 driver may require kernel-specific fixes.
- A basic USB audio dongle cannot drive the included unpowered 8 ohm speakers;
  fallback audio would require amplification or a powered USB speaker/speakerphone.
- Start voice interaction half-duplex: stop listening during TTS playback.
- N20 leads are thin; strain-relieve them without stressing motor tabs.
- One forward VL53L1X can miss corners and side obstacles; this is accepted for
  v1.
- The NoIR camera has unusual daylight colors and needs infrared illumination
  to see in darkness.
- Dupont wiring is suitable for prototyping, not a commercial product.
- Measure Pi temperature under load.
