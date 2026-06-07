from core.anims import led_animations
from core.plugins import led_animations_plugins
from core.anims_overides import led_animations_overides


class Config():
    def __init__(self):

        self.heartbeat_interval = 2

        self.led_animations = led_animations
        self.led_animations_plugins = led_animations_plugins
        self.led_animations_overides = led_animations_overides

        self.anims = {
            **led_animations,
            **led_animations_plugins,
            **led_animations_overides,
        }

    def reload_anims(self):
        """ TODO; Reload the plugin & anims """
        pass
