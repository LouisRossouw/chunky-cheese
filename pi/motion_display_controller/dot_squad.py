import requests


def run_dot_squad(anim, base_url="http://localhost:4001"):
    # Sanitize URL
    base_url = base_url.strip('"').strip("'")
    if not base_url.startswith("http"):
        base_url = f"http://{base_url}"

    # Ensure /run suffix if not present
    if not base_url.endswith("/run"):
        base_url = f"{base_url.rstrip('/')}/run"

    try:
        requests.post(
            f"{base_url}/{anim}", timeout=2)
    except Exception as e:
        # Silently fail, but could print if PRINT_LOGS was passed here
        pass
