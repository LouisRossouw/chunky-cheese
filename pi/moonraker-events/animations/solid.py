from animation import Animation

class Solid(Animation):

    def __init__(self, color):
        self.color = color

    def render(self, segment, pixels, printer_state=None):
        segment.fill(self.color, pixels)