import json
import asyncio
import argparse

from state import PrinterState
from moonraker import MoonrakerClient
from renderer import Renderer
from manager import LedManager


async def render_loop(renderer, state):
    print("LED Renderer loop started...")
    last_time = asyncio.get_event_loop().time()
    try:
        while True:
            current_time = asyncio.get_event_loop().time()
            dt = current_time - last_time
            last_time = current_time

            renderer.update(dt)
            renderer.render(state)

            # Target ~30 FPS (1/30 ≈ 0.033 seconds)
            await asyncio.sleep(0.033)
    except asyncio.CancelledError:
        print("LED Renderer loop stopped.")
    except Exception as e:
        print(f"Error in LED Renderer loop: {e}")
    finally:
        renderer.clear()


async def api_loop(app, host, port):
    """Run the FastAPI/uvicorn server as an asyncio-native task."""
    import uvicorn
    config = uvicorn.Config(app, host=host, port=port, log_level="info")
    server = uvicorn.Server(config)
    print(f"LED API starting on http://{host}:{port}  (docs: /docs)")
    await server.serve()


async def moonraker_loop(led_manager, state, app_state):
    """Subscribe to Moonraker events and update printer state / LED manager."""
    moonraker = MoonrakerClient()
    try:
        async with await moonraker.connect() as ws:
            print("Connected to Moonraker!")

            await ws.send(
                json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "method": "printer.objects.subscribe",
                        "params": {
                            "objects": {
                                "print_stats": None,
                                "virtual_sdcard": None,
                                "heater_bed": None,
                                "extruder": None,
                                "fan": None,
                                "toolhead": None,
                                "gcode_move": None,
                            }
                        },
                        "id": 1,
                    }
                )
            )
            while True:
                message = await ws.recv()
                msg = json.loads(message)

                if msg.get("method") == "notify_status_update":
                    state.update(msg)
                    # Only let Moonraker drive LEDs when in auto mode
                    if app_state.get("mode", "auto") == "auto":
                        led_manager.update(state)

    except asyncio.CancelledError:
        print("Moonraker loop cancelled.")
    except Exception as e:
        print(f"Moonraker connection error: {e}")


async def main():
    parser = argparse.ArgumentParser(description="Moonraker LED Controller")
    parser.add_argument(
        "--no-moonraker",
        action="store_true",
        help="Skip the Moonraker connection (useful for standalone API testing)",
    )
    parser.add_argument("--host", default="0.0.0.0", help="API server host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8080, help="API server port (default: 8080)")
    args = parser.parse_args()

    state = PrinterState()
    renderer = Renderer()
    led_manager = LedManager(renderer)

    # Build the FastAPI app – pass live objects so the API can control them
    from api import build_api
    app = build_api(renderer, led_manager, state)

    # Give moonraker_loop a reference to the same mode dict as the FastAPI app
    app_state = app.state.__dict__

    # Start the render loop as a background task
    render_task = asyncio.create_task(render_loop(renderer, state))

    # Always start the API server
    api_task = asyncio.create_task(api_loop(app, args.host, args.port))

    tasks = [render_task, api_task]

    if not args.no_moonraker:
        moonraker_task = asyncio.create_task(
            moonraker_loop(led_manager, state, app_state)
        )
        tasks.append(moonraker_task)
    else:
        print("Moonraker connection skipped (--no-moonraker flag set)")

    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("Shutdown requested...")
    finally:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        renderer.clear()


if __name__ == "__main__":
    asyncio.run(main())
