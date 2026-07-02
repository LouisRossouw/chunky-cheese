from animations.progress import Progress
from animations.z_tracker import ZTracker
from animations.temperature import Temperature
from animations.solid import Solid
from animations.heartbeat import Heartbeat
from animations.rainbow_cycle import RainbowCycle

class PrintingState:

    def apply(self, leds):
        leds.segment("front_left").animation = Solid((0, 0, 0))
        leds.segment("front_right").animation = Progress(color_active=(0, 255, 0), color_bg=(0, 0, 0), mode='print')
        leds.segment("heartbeat").animation = Heartbeat(color=(0, 200, 0))
        
        # Inside columns show Z tracker
        tracker = ZTracker(color=(0, 0, 255), reverse=True)
        leds.segment("inside_left").animation = tracker
        leds.segment("inside_right").animation = tracker
        
        leds.segment("inside_top_center").animation = RainbowCycle()
        leds.segment("center_top").animation = RainbowCycle()
        
        # Toolhead shows extruder heater temperature
        leds.segment("toolhead").animation = Temperature(sensor='extruder')

