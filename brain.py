# brain.py
import random

CRUISE, BACKUP, TURN = "cruise", "backup", "turn"

class Brain:
    def __init__(self):
        self.state = CRUISE      # what am I in the middle of?
        self.until = 0.0         # ...and until what time?
        self.turn_dir = 1        # +1 or -1, picked fresh each avoidance

    def decide(self, distance, t):
        """One tick: given sensor reading + current time, return (left, right)
        wheel speeds as fractions in -1..1."""

        if self.state == CRUISE:
            if distance is not None and distance < 220:
                self.state = BACKUP
                self.until = t + 0.6            # back up for 0.6 seconds
                return (0.0, 0.0)               # this tick: hard stop
            if distance is not None and distance < 450:
                return (0.35, 0.35)             # something's coming: creep
            return (0.7, 0.7)                   # open floor: cruise

        if self.state == BACKUP:
            if t >= self.until:
                self.state = TURN
                self.turn_dir = random.choice((-1, 1))
                self.until = t + random.uniform(0.5, 1.4)
            return (-0.4, -0.4)

        # state == TURN
        if t >= self.until and (distance is None or distance > 450):
            self.state = CRUISE
            return (0.7, 0.7)
        return (0.55 * self.turn_dir, -0.55 * self.turn_dir)