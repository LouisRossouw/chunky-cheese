from .boot import animation as boot
from .error import animation as error
from .notify_01 import animation as notify_01
from .notify_02 import animation as notify_02

led_animations = {
    "boot": boot,
    "error": error,
    "notify_01": notify_01,
    "notify_02": notify_02,
}
