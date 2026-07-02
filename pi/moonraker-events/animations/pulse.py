import math
from animation import Animation


class Pulse(Animation):

    def __init__(self, color, period=2.0):
        self.color = color
        self.period = period
        self.time = 0

    def update(self, dt):
        self.time = (self.time + dt) % self.period

    def render(self, segment, pixels, printer_state=None):
        # Brightness oscillates between 0.2 and 1.0 using sine wave
        factor = 0.6 + 0.4 * math.sin(2 * math.pi * self.time / self.period)
        r = int(self.color[0] * factor)
        g = int(self.color[1] * factor)
        b = int(self.color[2] * factor)
        segment.fill((r, g, b), pixels)