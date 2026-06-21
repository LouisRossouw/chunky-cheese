class PrinterState:
    def __init__(self):
        self.mode = "idle"
        self.progress = 0.0
        self.bed_power = 0
        self.nozzle_power = 0
        self.print_state = "standby"

    def update(self, msg):
        updates = msg["params"][0]

        ps = updates.get("print_stats", {})
        vs = updates.get("virtual_sdcard", {})
        bed = updates.get("heater_bed", {})
        ext = updates.get("extruder", {})

        # progress
        if "progress" in vs:
            self.progress = vs["progress"]

        # power tracking
        if "power" in bed:
            self.bed_power = bed["power"]

        if "power" in ext:
            self.nozzle_power = ext["power"]

        # persist print state if it appears
        if "state" in ps:
            self.print_state = ps["state"]
            # print(ps["state"])

        # -------------------------
        # MODE INFERENCE
        if self.print_state == "error":
            self.mode = "error"

        elif self.print_state == "complete":
            self.mode = "finished"

        elif self.print_state == "printing":
            self.mode = "printing"

        elif self.print_state == "standby":
            if self.bed_power > 0 or self.nozzle_power > 0:
                self.mode = "heating"
            else:
                self.mode = "idle"
