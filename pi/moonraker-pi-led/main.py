import asyncio
import json
# import pprint
from moonraker import MoonrakerClient
from state import PrinterState


async def main():
    moonraker = MoonrakerClient()
    state = PrinterState()

    async with await moonraker.connect() as ws:
        print("Connected!")

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
                            "fan": None
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

                print(state.mode, state.progress)
        # while True:
        #     message = await ws.recv()
        #     # print('\n\n')
        #     # pprint.pprint(json.loads(message))
        #     msg = json.loads(message)

        #     if msg.get("method") == "notify_status_update":
        #         updates = msg["params"][0]

        #         if "print_stats" in updates:
        #             print("STATE:", updates)

        #         if "virtual_sdcard" in updates:
        #             print("PROGRESS:", updates)


asyncio.run(main())
