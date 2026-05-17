import uuid
import requests
from config import GOVEE_API_KEY, GOVEE_BASE_URL, GOVEE_CONTENT_TYPE

class GoveeClient:
    def __init__(self, api_key: str = GOVEE_API_KEY, base_url: str = GOVEE_BASE_URL, content_type: str = GOVEE_CONTENT_TYPE):
        self.api_key = api_key
        self.base_url = base_url
        self.content_type = content_type
        self.headers = {
            "Content-Type": self.content_type,
            "Govee-API-Key": self.api_key,
        }

    # --- private helper: every control call goes through here ---
    def _control(self, sku: str, device_id: str, capability_type: str,
                 instance: str, value) -> dict:
        payload = {
            "requestId": str(uuid.uuid4()),
            "payload": {
                "sku": sku,
                "device": device_id,
                "capability": {
                    "type": capability_type,
                    "instance": instance,
                    "value": value,
                },
            },
        }
        resp = requests.post(
            f"{self.base_url}/router/api/v1/device/control",
            json=payload,
            headers=self.headers,
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()

    # --- public API: one method per logical action ---
    def turn_on(self, sku: str, device_id: str) -> dict:
        return self._control(sku, device_id,
                             "devices.capabilities.on_off", "powerSwitch", 1)

    def turn_off(self, sku: str, device_id: str) -> dict:
        return self._control(sku, device_id,
                             "devices.capabilities.on_off", "powerSwitch", 0)

    def set_color(self, sku: str, device_id: str, rgb: int) -> dict:
        return self._control(sku, device_id,
                             "devices.capabilities.color_setting", "colorRgb", rgb)

    def set_brightness(self, sku: str, device_id: str, pct: int) -> dict:
        if not 1 <= pct <= 100:
            raise ValueError("brightness must be 1–100")
        return self._control(sku, device_id,
                             "devices.capabilities.range", "brightness", pct)

    def get_devices(self) -> dict:
        resp = requests.get(
            f"{self.base_url}/router/api/v1/user/devices",
            headers=self.headers,
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
