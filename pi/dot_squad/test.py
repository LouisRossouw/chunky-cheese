from led_map import led_animations

if __name__ == "__main__":
    import requests

    # body = {
    #     "name": "motion_detected",
    #     "loop": False,
    #     "frames": led_animations.get('notify_01')
    # }

    # res = requests.post(
    #     url="http://10.0.0.158:4001/run-led-sequence",
    #     # json=body
    # )

    res = requests.post(
        url="http://10.0.0.158:4001/run-led/notify_01",
        # json=body
    )

    print("Status:", res.status_code)
