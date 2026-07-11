from animation import Animation

class Temperature(Animation):
    def __init__(self, sensor=None):
        self.sensor = sensor

    def render(self, segment, pixels, printer_state):
        # Auto-detect sensor if None
        sensor = self.sensor
        if not sensor:
            if "top" in segment.name:
                sensor = "bed"
            else:
                sensor = "extruder"

        temp = 0.0
        target = 0.0
        if printer_state:
            if sensor == "bed":
                temp = printer_state.heater_bed_temperature
                target = printer_state.target_heater_bed_temperature
            else:
                temp = printer_state.extruder_temperature
                target = printer_state.target_extruder_temperature

        if target <= 0:
            color = (0, 0, 50)  # Dim blue for cooldown/unheated
        else:
            pct = min(1.0, max(0.0, temp / target))
            # Cold (Blue) -> Hot (Red)
            r = int(255 * pct)
            g = 0
            b = int(255 * (1.0 - pct))
            color = (r, g, b)

        segment.fill(color, pixels)
