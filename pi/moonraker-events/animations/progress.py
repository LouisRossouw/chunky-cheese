from animation import Animation

class Progress(Animation):
    def __init__(self, color_active=(0, 255, 0), color_bg=(20, 20, 20), mode='print'):
        self.color_active = color_active
        self.color_bg = color_bg
        self.mode = mode

    def render(self, segment, pixels, printer_state):
        pct = 0.0
        if printer_state:
            if self.mode == 'print':
                # Progress is 0.0 to 1.0 or 0 to 100 from Moonraker
                pct = printer_state.progress * 100.0 if printer_state.progress <= 1.0 else printer_state.progress
            elif self.mode == 'bed':
                pct = printer_state.heater_bed_target_progress
            elif self.mode == 'extruder':
                pct = printer_state.extruder_target_progress

        pct = max(0.0, min(100.0, pct))
        num_lit = int((pct / 100.0) * segment.length)

        for i in range(segment.length):
            if i < num_lit:
                segment.set_pixel(i, self.color_active, pixels)
            else:
                segment.set_pixel(i, self.color_bg, pixels)
