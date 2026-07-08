from animation import Animation


def _wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    pos = pos & 255
    if pos < 85:
        return (int(pos * 3), int(255 - pos * 3), 0)
    elif pos < 170:
        pos -= 85
        return (int(255 - pos * 3), 0, int(pos * 3))
    else:
        pos -= 170
        return (0, int(pos * 3), int(255 - pos * 3))


class RainbowCycle(Animation):
    """Rainbow wave that cycles across the entire segment.

    Args:
        speed: How many hue-degrees to advance per second (default 60 → full
               cycle every ~4 seconds).
    """

    def __init__(self, speed=60.0):
        self._hue_offset = 0.0
        self.speed = speed

    def update(self, dt):
        self._hue_offset = (self._hue_offset + self.speed * dt) % 256.0

    def render(self, segment, pixels, printer_state=None):
        n = segment.length
        for i in range(n):
            pixel_index = int((i * 256 / n) + self._hue_offset) & 255
            segment.set_pixel(i, _wheel(pixel_index), pixels)
