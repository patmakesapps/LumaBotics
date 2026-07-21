# robot.py -- the REAL robot's entry point.
# Reads the VL53L1X sensor and sends the distance into Brain.
# Motor output is intentionally disabled until the Motor HAT is connected.

import time

import board
import adafruit_vl53l1x

from brain import Brain

# Create the Raspberry Pi I2C connection.
i2c = board.I2C()

# Connect to the VL53L1X at its default I2C address, 0x29.
sensor = adafruit_vl53l1x.VL53L1X(i2c)

# Short-distance mode is well suited for obstacle avoidance.
sensor.distance_mode = 1

# Each measurement is allowed up to 100 milliseconds.
sensor.timing_budget = 100


def read_sensor():
    """
    Read the VL53L1X distance sensor.

    The Adafruit library returns centimeters.
    Brain expects millimeters, so the value is multiplied by 10.

    Returns:
        int: Distance in millimeters.
        None: No valid reading was available.
    """

    # Do not wait forever if the sensor fails to provide new data.
    deadline = time.monotonic() + 0.25

    while not sensor.data_ready:
        if time.monotonic() >= deadline:
            return None

        time.sleep(0.005)

    distance_cm = sensor.distance

    # Tell the sensor that this reading has been handled.
    sensor.clear_interrupt()

    if distance_cm is None:
        return None

    distance_mm = int(round(distance_cm * 10))

    return distance_mm


def set_motors(left, right):
    """
    Motor control placeholder.

    left and right are values from -1.0 to 1.0.

    This currently does nothing so the Brain can be tested safely
    before the Motor HAT and motor battery are connected.
    """

    # TODO: Write PWM commands to the Motor HAT.
    pass


brain = Brain()

# Begin continuous distance measurements.
sensor.start_ranging()

last_status_print = 0.0

try:
    while True:
        current_time = time.monotonic()

        distance_mm = read_sensor()  # SENSE
        left, right = brain.decide(distance_mm, current_time)  # DECIDE
        set_motors(left, right)  # ACT

        # Print status four times per second instead of flooding the terminal.
        if current_time - last_status_print >= 0.25:
            distance_text = (
                f"{distance_mm} mm" if distance_mm is not None else "no reading"
            )

            print(
                f"distance={distance_text:<12} "
                f"state={brain.state:<6} "
                f"left={left:+.2f} "
                f"right={right:+.2f}"
            )

            last_status_print = current_time

        time.sleep(0.05)

except KeyboardInterrupt:
    print("\nStopping LumaBot.")

finally:
    # Always stop the sensor cleanly when the program exits.
    sensor.stop_ranging()
