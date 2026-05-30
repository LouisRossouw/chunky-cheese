import os
from core.utils import read_json

led_animations = {}

this_dir = os.path.dirname(__file__)
anims_list = os.listdir(this_dir)

for anim in anims_list:
    ext = anim.split(".")[-1]
    name = anim.replace(f".{ext}", '')

    if ext == "json":
        led_animations[name] = read_json(os.path.join(this_dir, anim))
