# device.py - переработанный класс устройства
import json
import logging

_LOGGER = logging.getLogger('harvia_sauna')

class HarviaDevice:
    def __init__(self, api, device_id, initial_data=None):
        self.api = api
        self.id = device_id
        self.name = initial_data.get('name', 'Harvia Sauna')
        self.state = initial_data.get('state', {})
        self.callbacks = []

    async def update_state(self, new_state):
        """Update device state and notify subscribers"""
        self.state.update(new_state)
        await self._notify_subscribers()
        return await self.api.update_device_state(self.id, self.state)

    async def fetch_state(self):
        """Fetch current state from server"""
        self.state = await self.api.get_device_state(self.id)
        await self._notify_subscribers()
        return self.state

    def register_callback(self, callback):
        """Register callback for state updates"""
        self.callbacks.append(callback)

    async def _notify_subscribers(self):
        """Notify all registered callbacks"""
        for callback in self.callbacks:
            try:
                await callback(self.state)
            except Exception as e:
                _LOGGER.error(f"Callback error: {str(e)}")

    async def set_power(self, state):
        """Turn device on/off"""
        return await self.update_state({'power': state})

    async def set_temperature(self, temperature):
        """Set target temperature"""
        return await self.update_state({'target_temp': temperature})

    async def set_light(self, state):
        """Control light"""
        return await self.update_state({'light': state})

    async def set_fan(self, state):
        """Control fan"""
        return await self.update_state({'fan': state})