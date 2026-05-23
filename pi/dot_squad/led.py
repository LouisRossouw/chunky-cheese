import time
import board
import neopixel
import threading

from led_map import led_animations

pixels = neopixel.NeoPixel(board.D18, 3)
led_lock = threading.Lock()


def run(frames):
    """ Runs the led frame sequence """

    with led_lock:
        for frame in frames:
            colors = frame['colors']
            duration = frame['duration']

            for i, color in enumerate(colors):
                pixels[i] = color

            time.sleep(duration)


def clear():
    with led_lock:
        pixels.fill((0, 0, 0))


if __name__ == "__main__":
    while True:
        time.sleep(1)
        run(led_animations.get("notify_02"))
