# robot.py -- the REAL robot's entry point. Runs on the Pi on July 19th.
import time
from brain import Brain


def read_sensor():
    # TODO chunk 4: read the VL53L1X over I2C, return mm or None
    raise NotImplementedError("no hardware yet")


def set_motors(left, right):
    # TODO chunk 5: write PWM duty cycles to the motor chip over I2C
    raise NotImplementedError("no hardware yet")


brain = Brain()

while True:                          # robots don't have a step 2000
    t = time.monotonic()             # real seconds from a real clock
    d = read_sensor()                # SENSE
    left, right = brain.decide(d, t) # DECIDE  <-- identical line to sim.py
    set_motors(left, right)          # ACT
    time.sleep(0.05)                 # ~20 ticks per second