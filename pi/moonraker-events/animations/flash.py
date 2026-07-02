from animation import Animation

class Flash(Animation):
    def __init__(self, color, period=1.0):
        self.color = color
        self.period = period
        self.time = 0

    def update(self, dt):
        self.time = (self.time + dt) % self.period

    def render(self, segment, pixels, printer_state=None):
        # ON for half the period, OFF for the other half
        if self.time < self.period / 2.0:
            segment.fill(self.color, pixels)
        else:
            segment.fill((0, 0, 0), pixels)
