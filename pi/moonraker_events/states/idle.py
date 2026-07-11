from animations.solid import Solid
from animations.heartbeat import Heartbeat

class IdleState:

    def apply(self, leds):
        leds.segment("heartbeat").animation = Heartbeat(color=(0, 0, 200))

        off = Solid((0, 0, 0))
        leds.segment("inside_left").animation = off
        leds.segment("inside_right").animation = off
        leds.segment("inside_top_center").animation = off
        leds.segment("center_top").animation = off
        leds.segment("toolhead").animation = off
