from animation import Animation

class ZTracker(Animation):
    def __init__(self, color=(255, 255, 0), bg_color=(0, 0, 0)):
        self.color = color
        self.bg_color = bg_color

    def render(self, segment, pixels, printer_state):
        z = 0.0
        max_z = 250.0  # default fallback maximum Z height in mm

        if printer_state:
            z = printer_state.z_position
            if printer_state.max_z > 0:
                max_z = printer_state.max_z

        pct = max(0.0, min(1.0, z / max_z))
        led_idx = int(pct * (segment.length - 1))

        for i in range(segment.length):
            if i == led_idx:
                segment.set_pixel(i, self.color, pixels)
            elif abs(i - led_idx) == 1:
                # Dim glow flanking the bead
                dim = (self.color[0] // 3, self.color[1] // 3, self.color[2] // 3)
                segment.set_pixel(i, dim, pixels)
            else:
                segment.set_pixel(i, self.bg_color, pixels)
