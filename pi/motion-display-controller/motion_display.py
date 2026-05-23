import os
import time
import requests
import configparser

from gpiozero import MotionSensor

# CONFIG
config = configparser.ConfigParser(inline_comment_prefixes=('#', ';'))
config.read("/opt/motion-display-controller/config/motion.conf")

GPIO_PIN = config["DEFAULT"].getint("GPIO_PIN", 4)

ON = config["DEFAULT"].getint("BRIGHTNESS_ON", 255)
DIM = config["DEFAULT"].getint("BRIGHTNESS_DIM", 20)
OFF = config["DEFAULT"].getint("BRIGHTNESS_OFF", 0)

DIM_AFTER = config["DEFAULT"].getint("DIM_AFTER", 10)
OFF_AFTER = config["DEFAULT"].getint("OFF_AFTER", 20)

LOOP_DELAY = config["DEFAULT"].getint("LOOP_DELAY", 1)
FADE_STEP = config["DEFAULT"].getint("FADE_STEP", 5)
FADE_DELAY = config["DEFAULT"].getfloat("FADE_DELAY", 0.01)
PRINT_LOGS = config["DEFAULT"].getboolean("PRINT_LOGS", False)

BRIGHTNESS_PATH = config["DEFAULT"].get(
    "BRIGHTNESS_PATH",
    "/sys/class/backlight/10-0045/brightness"
)

# PRE-FLIGHT CHECK
if not os.path.exists(BRIGHTNESS_PATH):
    print(f"CRITICAL ERROR: Backlight path not found at {BRIGHTNESS_PATH}")
    print("Please check your configuration or hardware drivers.")
    exit(1)


# VALIDATION
def validate_brightness(*values):
    for value in values:
        if not (0 <= value <= 255):
            raise ValueError("Brightness values must be between 0 and 255")


validate_brightness(ON, DIM, OFF)

# SETUP
pir = MotionSensor(GPIO_PIN)

current_brightness = OFF
last_motion = time.time()
is_dimmed = False
is_on = False


# BRIGHTNESS CONTROL
def set_brightness(value):
    try:
        with open(BRIGHTNESS_PATH, "w") as f:
            f.write(str(value))
    except PermissionError:
        print(
            f"PERMISSION ERROR: Cannot write to {BRIGHTNESS_PATH}. Is the service running with correct permissions?")
        exit(1)
    except Exception as e:
        print(f"ERROR: Failed to set brightness: {e}")


def fade_to(target):
    global current_brightness

    while current_brightness != target:
        if current_brightness < target:
            current_brightness = min(current_brightness + FADE_STEP, target)
        else:
            current_brightness = max(current_brightness - FADE_STEP, target)

        set_brightness(current_brightness)
        time.sleep(FADE_DELAY)


# STARTUP
print("Starting motion display service...")
fade_to(ON)
is_on = True


# MAIN LOOP
while True:
    if pir.motion_detected:
        last_motion = time.time()

        if not is_on or is_dimmed:
            fade_to(ON)
            is_on = True
            is_dimmed = False

            if PRINT_LOGS:
                print("Motion detected → Full brightness")

            # Trigger Dot Squad LED notification
            try:
                requests.post("http://localhost:4001/run-led/boot", timeout=2)
            except Exception as e:
                if PRINT_LOGS:
                    print(f"API Notification failed: {e}")

    diff = time.time() - last_motion

    # Dim
    if diff > DIM_AFTER:
        if is_on and not is_dimmed:
            fade_to(DIM)
            is_dimmed = True

            if PRINT_LOGS:
                print("No motion → Dim")

    # Turn Off
    if diff > OFF_AFTER:
        if is_on:
            fade_to(OFF)
            is_on = False
            is_dimmed = False

            if PRINT_LOGS:
                print("No motion → Off")

    time.sleep(LOOP_DELAY)
