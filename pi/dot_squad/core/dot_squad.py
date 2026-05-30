import time
import board
import neopixel
import threading

pixels = neopixel.NeoPixel(board.D18, 3)
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
                    pixels[i] = color

                time.sleep(duration)

    def heartbeat_loop(self):
        """ General heartbeat to show the service is running. """

        while True:
            self.run(self.anims.get('heartbeat'))
            time.sleep(2)

    def clear(self):
        """ Clears neopixel """

        with led_lock:
            pixels.fill((0, 0, 0))


if __name__ == "__main__":
    from config import Config

    DS = DotSquad()
    config = Config()

    while True:
        time.sleep(1)
        DS.run(config.anims.get("notify_02"))
