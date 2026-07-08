from animation import Animation

class HeatingProgress(Animation):
    def __init__(self, mode='bed', color_bg=(0, 0, 0)):
        self.mode = mode
        self.color_bg = color_bg

    def render(self, segment, pixels, printer_state):
        pct = 0.0
        if printer_state:
            if self.mode == 'bed':
                pct = printer_state.heater_bed_target_progress
            elif self.mode == 'extruder':
                pct = printer_state.extruder_target_progress

        pct = max(0.0, min(100.0, pct))
        t = pct / 100.0

        # Linear color transition from Red (255, 0, 0) at 0% to Green (0, 255, 0) at 100%
        r = int(255 * (1.0 - t))
        g = int(255 * t)
        b = 0
        color_active = (r, g, b)

        num_lit = int(t * segment.length)

        for i in range(segment.length):
            if i < num_lit:
                segment.set_pixel(i, color_active, pixels)
            else:
                segment.set_pixel(i, self.color_bg, pixels)
