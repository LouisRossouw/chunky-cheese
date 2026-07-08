from animation import Animation


class ColorWipe(Animation):
    """Fills the segment one pixel at a time, then erases it the same way.

    Args:
        color:  RGB tuple to paint.
        speed:  Pixels per second to advance the wipe (default 20).
    """

    def __init__(self, color=(0, 200, 255), speed=20.0):
        self.color = color
        self.speed = speed
        self._progress = 0.0   # 0 → 2*n: first half fills, second half clears
        self._phase = "fill"   # "fill" or "clear"

    def update(self, dt):
        self._progress += self.speed * dt

    def render(self, segment, pixels, printer_state=None):
        n = segment.length

        # Reset when a full fill+clear cycle is done
        total = n * 2
        progress = self._progress % total
        head = int(progress)

        if head < n:
            # Fill phase: light up up to `head` pixels
            for i in range(n):
                if i <= head:
                    segment.set_pixel(i, self.color, pixels)
                else:
                    segment.set_pixel(i, (0, 0, 0), pixels)
        else:
            # Clear phase: erase from the front
            clear_head = head - n
            for i in range(n):
                if i <= clear_head:
                    segment.set_pixel(i, (0, 0, 0), pixels)
                else:
                    segment.set_pixel(i, self.color, pixels)
