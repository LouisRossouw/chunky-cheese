from animations.flash import Flash
from animations.heartbeat import Heartbeat

class ErrorState:

    def apply(self, leds):
        flash = Flash((255, 0, 0))

        leds.segment("front_left").animation = flash
        leds.segment("front_right").animation = flash
        leds.segment("inside_left").animation = flash
        leds.segment("inside_right").animation = flash
        leds.segment("inside_top_center").animation = flash
        leds.segment("center_top").animation = flash
        leds.segment("toolhead").animation = flash

        # In error state, heartbeat blinks red quickly (1.0s period)
        leds.segment("heartbeat").animation = Heartbeat(color=(255, 0, 0), period=1.0)