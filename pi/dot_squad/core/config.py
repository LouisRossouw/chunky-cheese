from core.anims import led_animations
from core.plugins import led_animations_plugins


class Config():
    def __init__(self):

        self.led_animations_plugins = led_animations_plugins
        self.led_animations = led_animations

        self.anims = {
            **led_animations_plugins,
            **led_animations,
        }

    def reload_anims(self):
        """ TODO; Reload the plugin & anims """
        pass
