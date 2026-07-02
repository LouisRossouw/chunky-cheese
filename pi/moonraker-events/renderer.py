import board
import neopixel
import threading


from segment import Segment
from utils import read_json


PIXEL_COUNT = 120
PIXEL_PIN = board.D18

pixels = neopixel.NeoPixel(PIXEL_PIN, PIXEL_COUNT, auto_write=False)
led_lock = threading.Lock()

segments_config = read_json('segments.json') or []


class Renderer:
    def __init__(self):
        # Configure printer segments matching the physical LED strip setup
        self.segments = build_segments(segments_config)

    def update(self, dt):
        """Ticks the animations running on active segments by the delta time."""
        for segment in self.segments.values():
            if segment.enabled and segment.animation:
                segment.animation.update(dt)

    def render(self, printer_state):
        """Draws current animation frames onto the NeoPixel buffer."""
        with led_lock:
            # Turn everything black by default in buffer
            pixels.fill((0, 0, 0))

            # Render each enabled segment's active animation
            for segment in self.segments.values():
                if segment.enabled and segment.animation:
                    segment.animation.render(segment, pixels, printer_state)

            pixels.show()

    def clear(self):
        """Turns off all physical LEDs."""
        with led_lock:
            pixels.fill((0, 0, 0))
            pixels.show()


def build_segments(config):

    segments = {}
    for seg in segments_config:
        name = seg.get("name")
        start_led = seg.get("start_led")
        end_led = seg.get("end_led")
        reverse = seg.get("reverse")

        segments[name] = Segment(name, start_led, end_led, reverse)
    return segments
