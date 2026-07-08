class Segment:
    def __init__(self, name, start, end, reverse=False):
        self.name = name
        self.start = start
        self.end = end
        self.reverse = reverse
        self._animation = None
        self.enabled = True

    @property
    def length(self):
        return self.end - self.start + 1

    @property
    def animation(self):
        return self._animation

    @animation.setter
    def animation(self, anim):
        self._animation = anim

    def set_pixel(self, relative_index, color, pixels):
        """Sets a pixel relative to the start of this segment."""
        if 0 <= relative_index < self.length:
            if self.reverse:
                absolute_index = self.end - relative_index
            else:
                absolute_index = self.start + relative_index
            pixels[absolute_index] = color

    def fill(self, color, pixels):
        """Fills the entire segment with a solid color."""
        for i in range(self.start, self.end + 1):
            pixels[i] = color
