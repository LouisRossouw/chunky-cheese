from animation import Animation


class Comet(Animation):
    """A bright comet head with a decaying tail that bounces back and forth.

    Args:
        color:     RGB tuple for the comet color.
        tail_len:  Number of pixels in the tail (default 5).
        speed:     Pixels per second the comet travels (default 30).
    """

    def __init__(self, color=(255, 100, 20), tail_len=5, speed=30.0):
        self.color = color
        self.tail_len = tail_len
        self.speed = speed
        self._pos = 0.0
        self._direction = 1

    def update(self, dt):
        self._pos += self._direction * self.speed * dt

    def render(self, segment, pixels, printer_state=None):
        n = segment.length

        # Clamp and bounce
        if self._pos >= n - 1:
            self._pos = n - 1
            self._direction = -1
        elif self._pos < 0:
            self._pos = 0
            self._direction = 1

        head = int(self._pos)

        # Clear the segment first
        segment.fill((0, 0, 0), pixels)

        # Draw the head + tail
        for t in range(self.tail_len + 1):
            idx = head - t * self._direction
            if 0 <= idx < n:
                # Tail decays in brightness exponentially
                decay = (1.0 - t / (self.tail_len + 1)) ** 2
                r = int(self.color[0] * decay)
                g = int(self.color[1] * decay)
                b = int(self.color[2] * decay)
                segment.set_pixel(idx, (r, g, b), pixels)
