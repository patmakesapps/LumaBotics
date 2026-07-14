# sim.py
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import math
import turtle
from sensor import ray_cast
from brain import Brain

screen = turtle.Screen()
screen.setup(700, 550)
screen.title("lumabot sim")

bot = turtle.Turtle()
bot.shape("turtle")

SCALE = 0.25
MAXV = 234.0

walls = [                                    # a 2m x 1.6m room, origin at center
    (-1000, -800, 1000, -800),
    (1000, -800, 1000, 800),
    (1000, 800, -1000, 800),
    (-1000, 800, -1000, -800),
]

def add_box(x, y, w, h):                     # <-- new
    """Add a rectangular obstacle: corner at (x, y), w wide, h tall."""
    walls.append((x,     y,     x + w, y    ))   # bottom
    walls.append((x + w, y,     x + w, y + h))   # right
    walls.append((x + w, y + h, x,     y + h))   # top
    walls.append((x,     y + h, x,     y    ))   # left

add_box(200, 100, 400, 250)                  # <-- new: couch
add_box(-700, -500, 300, 200)                # <-- new: coffee table
add_box(-100, 400, 150, 300)                 # <-- new: bookshelf

walls.append((300, -300, 700, -300))         # <-- new: U-trap, bottom arm
walls.append((700, -300, 700,  100))         # <-- new: U-trap, back wall
walls.append((700,  100, 300,  100))         # <-- new: U-trap, top arm (mouth opens left)

pen = turtle.Turtle(); pen.hideturtle(); pen.penup()
for (x1, y1, x2, y2) in walls:
    pen.goto(x1 * SCALE, y1 * SCALE); pen.pendown()
    pen.goto(x2 * SCALE, y2 * SCALE); pen.penup()

def read_sensor(x, y, theta):
    hits = [d for w in walls if (d := ray_cast(x, y, theta, w)) is not None]
    return min(hits) if hits else None

brain = Brain()
x, y, theta = 0.0, 0.0, 0.3
TRACK, dt = 120.0, 0.05

for i in range(6000):                        # <-- new: 300 seconds, traps need time
    t = i * dt
    d = read_sensor(x, y, theta)
    left, right = brain.decide(d, t)         # fractions in -1..1
    vl, vr = left * MAXV, right * MAXV       # -> mm/s at the boundary

    v = (vl + vr) / 2
    omega = (vr - vl) / TRACK
    theta += omega * dt
    x += v * math.cos(theta) * dt
    y += v * math.sin(theta) * dt

    screen.title(f"lumabot sim   {brain.state}   sensor: {d:.0f} mm" if d else f"lumabot sim   {brain.state}")
    bot.goto(x * SCALE, y * SCALE)
    bot.setheading(math.degrees(theta))

turtle.done()