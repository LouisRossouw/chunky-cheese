


class PrinterState:
    def __init__(self):
        self.progress = 0
        self.print_state = 'idle'

        self.extruder_temperature = 0
        self.target_extruder_temperature = 0
        self.extruder_target_progress = 0

        self.heater_bed_temperature = 0
        self.target_heater_bed_temperature = 0
        self.heater_bed_target_progress = 0

        self.z_position = 0.0
        self.max_z = 250.0  # Default fallback maximum Z height in mm

    def update(self, msg):
        params = msg["params"][0]

        print_stats = params.get('print_stats', {})
        virtual_sdcard = params.get('virtual_sdcard', {})
        progress = virtual_sdcard.get('progress')
        print_state = print_stats.get('state')

        # Bed
        heater_bed = params.get('heater_bed', {})
        heater_bed_temperature = heater_bed.get('temperature')
        target_heater_bed_temperature = heater_bed.get('target')

        # Extruder
        extruder = params.get('extruder', {})
        extruder_temperature = extruder.get('temperature')
        target_extruder_temperature = extruder.get('target')

        # Toolhead & GCode Move (Z-height tracking)
        toolhead = params.get('toolhead', {})
        gcode_move = params.get('gcode_move', {})

        position = toolhead.get('position')
        if position and len(position) >= 3:
            self.z_position = position[2]
        else:
            gcode_pos = gcode_move.get('gcode_position')
            if gcode_pos and len(gcode_pos) >= 3:
                self.z_position = gcode_pos[2]

        axis_max = toolhead.get('axis_maximum')
        if axis_max and len(axis_max) >= 3:
            self.max_z = axis_max[2]

        # Update values
        if print_state:
            self.print_state = print_state

        if progress is not None:
            self.progress = progress

        if target_extruder_temperature is not None:
            self.target_extruder_temperature = target_extruder_temperature

        if extruder_temperature is not None:
            self.extruder_temperature = extruder_temperature
            self.extruder_target_progress = (extruder_temperature / self.target_extruder_temperature) * 100 if self.target_extruder_temperature > 0 else 0

        if target_heater_bed_temperature is not None:
            self.target_heater_bed_temperature = target_heater_bed_temperature

        if heater_bed_temperature is not None:
            self.heater_bed_temperature = heater_bed_temperature
            self.heater_bed_target_progress = (heater_bed_temperature / self.target_heater_bed_temperature) * 100 if self.target_heater_bed_temperature > 0 else 0


