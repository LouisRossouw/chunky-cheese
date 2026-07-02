from animations.solid import Solid
from animations.breathe import Breathe
from animations.heating_progress import HeatingProgress
from animations.temperature import Temperature
from animations.heartbeat import Heartbeat

class HeatingState:
    def apply(self, leds):

        leds.segment("front_left").animation = HeatingProgress(mode='bed')
        leds.segment("front_right").animation = HeatingProgress(mode='extruder')
        leds.segment("heartbeat").animation = Heartbeat(color=(0, 0, 200))

        # Inside segments are solid red during pre-heating
        red = Breathe((255, 0, 0))
        
        leds.segment("inside_left").animation = red
        leds.segment("inside_right").animation = red

        # Toolhead shows the active extruder temperature curve
        leds.segment("toolhead").animation = Temperature(sensor='extruder')
