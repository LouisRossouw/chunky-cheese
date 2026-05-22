import time
import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 3)


def run(frames):
    """ Runs the led frame sequence """

    for frame in frames:
        colors = frame['colors']
        duration = frame['duration']

        for i, color in enumerate(colors):
            pixels[i] = color

        time.sleep(duration)


def clear():
    pixels.fill((0, 0, 0))


if __name__ == "__main__":

    while True:
        time.sleep(1)
        run([
        {"colors": [(255, 0, 0), (255, 0, 230), (0, 0, 255)], "duration": 0.05},  # nopep8
        {"colors": [(214, 250, 255), (214, 250, 255), (214, 250, 255)], "duration": 0.05},  # nopep8
    ])
