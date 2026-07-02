import random
from animation import Animation


class Sparkle(Animation):
    """Random pixels flash at full brightness over a dim base color.

    Args:
        color:       RGB tuple for the sparkle colour.
        base_dim:    Fraction (0–1) of colour used as the background glow
                     (default 0.05 → nearly off).
        density:     Average fraction of pixels sparkling per second
                     (default 0.3 → 30 % of pixels fire per second).
        flash_time:  How long each sparkle stays lit in seconds (default 0.08).
    """

    def __init__(self, color=(255, 255, 255), base_dim=0.05, density=0.3, flash_time=0.08):
        self.color = color
        self.base_dim = base_dim
        self.density = density
        self.flash_time = flash_time
        # dict of { pixel_index: time_remaining }
        self._active: dict[int, float] = {}

    def update(self, dt):
        # Decay existing sparkles
        expired = [k for k, v in self._active.items() if v - dt <= 0]
        for k in expired:
            del self._active[k]
        for k in self._active:
            self._active[k] -= dt

    def render(self, segment, pixels, printer_state=None):
        n = segment.length

        # Spawn new sparkles probabilistically
        for i in range(n):
            if i not in self._active and random.random() < self.density / n:
                self._active[i] = self.flash_time

        # Render: base glow for all pixels, bright for active sparkles
        base_r = int(self.color[0] * self.base_dim)
        base_g = int(self.color[1] * self.base_dim)
        base_b = int(self.color[2] * self.base_dim)

        for i in range(n):
            if i in self._active:
                segment.set_pixel(i, self.color, pixels)
            else:
                segment.set_pixel(i, (base_r, base_g, base_b), pixels)
