import time
# import board
# import neopixel
import threading

from core.anims import led_animations

# pixels = neopixel.NeoPixel(board.D18, 3)
led_lock = threading.Lock()


class DotSquad():
    def __init__(self, config):
        self.anims = config.anims

    def run(self, frames):
        """ Runs the led frame sequence """

        with led_lock:
            for frame in frames:
                colors = frame['colors']
                duration = frame['duration']

                for i, color in enumerate(colors):
                    print(color)
                    # pixels[i] = color

                time.sleep(duration)

    def heartbeat_loop(self):
        while True:
            self.run(self.anims.get('heartbeat'))
            time.sleep(2)

    def clear(self):
        with led_lock:
            # pixels.fill((0, 0, 0))
            print("clear clear")


if __name__ == "__main__":
    DS = DotSquad()

    while True:
        time.sleep(1)
        DS.run(led_animations.get("notify_02"))
