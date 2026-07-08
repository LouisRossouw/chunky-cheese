class Animation:
    def update(self, dt):
        """
        Updates the internal state of the animation over time.
        dt is the time elapsed since the last frame in seconds.
        """
        pass

    def render(self, segment, pixels, printer_state):
        """
        Renders the animation onto a specific NeoPixel segment.
        :param segment: The Segment object being rendered to.
        :param pixels: The NeoPixel strip (or mock strip) to write color values into.
        :param printer_state: The PrinterState object containing current telemetry.
        """
        raise NotImplementedError("Animations must implement the render method.")
