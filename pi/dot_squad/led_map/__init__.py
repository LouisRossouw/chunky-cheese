from .boot import animation as boot
from .error import animation as error
from .notify_01 import animation as notify_01
from .notify_02 import animation as notify_02
from .heartbeat import animation as heartbeat
from .motion_detected import animation as motion_detected
from .motion_dim import animation as motion_dim
from .motion_off import animation as motion_off

led_animations = {
    "boot": boot,
    "error": error,
    "notify_01": notify_01,
    "notify_02": notify_02,
    "heartbeat": heartbeat,
    "motion_detected": motion_detected,
    "motion_dim": motion_dim,
    "motion_off": motion_off,
}
