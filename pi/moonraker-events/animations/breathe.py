import math
from animation import Animation

class Breathe(Animation):
    def __init__(self, color, period=4.0):
        self.color = color
        self.period = period
        self.time = 0

    def update(self, dt):
        self.time = (self.time + dt) % self.period

    def render(self, segment, pixels, printer_state=None):
        # Soft sine wave fade from 5% to 100% brightness
        val = (math.sin(2 * math.pi * self.time / self.period) + 1.0) / 2.0
        brightness = 0.05 + 0.95 * val
        r = int(self.color[0] * brightness)
        g = int(self.color[1] * brightness)
        b = int(self.color[2] * brightness)
        segment.fill((r, g, b), pixels)
