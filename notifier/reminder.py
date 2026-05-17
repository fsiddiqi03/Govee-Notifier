import sys
import time

from clients.govee_client import GoveeClient
from config import DEVICES, FLASHING_CONFIG


def flash_reminder(event_type: str) -> None:
    client = GoveeClient()

    desk = DEVICES["desk"]
    sku, dev = desk["sku"], desk["device_id"]

    event = FLASHING_CONFIG[event_type]
    flash_brightness, flash_color, flash_cycles, flash_interval = event["brightness"], event["color_rgb"], event["cycles"], event["interval_seconds"]

    client.set_brightness(sku, dev, flash_brightness)
    client.set_color(sku, dev, flash_color)

    for _ in range(flash_cycles):
        client.turn_on(sku, dev)
        time.sleep(flash_interval)
        client.turn_off(sku, dev)
        time.sleep(flash_interval)


if __name__ == "__main__":
    event_type = sys.argv[1] if len(sys.argv) > 1 else "default"
    flash_reminder(event_type)
