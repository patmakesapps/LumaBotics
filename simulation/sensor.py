# sensor.py
import math

def ray_cast(x, y, theta, wall):
    x1, y1, x2, y2 = wall
    dx, dy = math.cos(theta), math.sin(theta)
    ex, ey = x2 - x1, y2 - y1
    denom = dx * ey - dy * ex
    if abs(denom) < 1e-9:
        return None
    t = ((x1 - x) * ey - (y1 - y) * ex) / denom
    u = ((x1 - x) * dy - (y1 - y) * dx) / denom
    if t > 0 and 0 <= u <= 1:
        return t
    return None

if __name__ == "__main__":
    wall = (500, -100, 500, 100)
    print(ray_cast(0, 0, 0.0, wall))
    print(ray_cast(100, 0, 0.0, wall))
    print(ray_cast(0, 0, math.pi, wall))
    print(ray_cast(0, 0, math.pi / 2, wall))