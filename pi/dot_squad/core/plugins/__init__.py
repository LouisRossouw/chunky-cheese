from pathlib import Path
import importlib.util

led_animations_plugins = {}

plugins_dir = Path(__file__).parent

for file in plugins_dir.glob("*.py"):
    if file.name == "__init__.py":
        continue

    spec = importlib.util.spec_from_file_location(
        file.stem,
        file,
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    led_animations_plugins[file.stem] = module.animation
