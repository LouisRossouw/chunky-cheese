from animation import Animation

class Heartbeat(Animation):
    def __init__(self, color=(0, 200, 0), period=2.0):
        self.color = color
        self.period = period
        self.time = 0

    def update(self, dt):
        self.time = (self.time + dt) % self.period

    def render(self, segment, pixels, printer_state=None):
        # Double-blink pulse: ON, OFF, ON, OFF...
        if 0.0 <= self.time < 0.15 or 0.3 <= self.time < 0.45:
            segment.fill(self.color, pixels)
        else:
            segment.fill((0, 0, 0), pixels)
