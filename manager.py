# manager.py - менеджер устройств
import logging
from typing import List
from .device import HarviaDevice

_LOGGER = logging.getLogger('harvia_sauna')

class DeviceManager:
    def __init__(self, api):
        self.api = api
        self.devices = {}

    async def initialize(self):
        """Initialize all devices"""
        devices_data = await self.api.get_devices()
        for device_data in devices_data:
            device = HarviaDevice(
                self.api,
                device_data['id'],
                device_data
            )
            self.devices[device.id] = device
            await device.fetch_state()
        return self.devices

    async def get_device(self, device_id) -> HarviaDevice:
        """Get device by ID"""
        if device_id not in self.devices:
            device = HarviaDevice(self.api, device_id)
            await device.fetch_state()
            self.devices[device_id] = device
        return self.devices[device_id]

    async def get_all_devices(self) -> List[HarviaDevice]:
        """Get all devices"""
        return list(self.devices.values())