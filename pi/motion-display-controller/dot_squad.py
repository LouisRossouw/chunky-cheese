import requests

# Temp hardcode
base_url = "http://localhost:4001/run"


def run_dot_squad(anim):
    try:
        requests.post(
            f"{base_url}/{anim}", timeout=2)
    except Exception:
        pass
