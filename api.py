# api.py - новый вариант для работы с Django API
import json
import logging
import aiohttp
from urllib.parse import urljoin

_LOGGER = logging.getLogger('harvia_sauna')

class HarviaDjangoAPI:
    def __init__(self, base_url, auth_token):
        self.base_url = base_url
        self.auth_token = auth_token
        self.session = aiohttp.ClientSession()
        self.headers = {
            'Authorization': f'Token {self.auth_token}',
            'Content-Type': 'application/json'
        }

    async def _request(self, method, endpoint, data=None):
        url = urljoin(self.base_url, endpoint)
        try:
            async with self.session.request(
                method,
                url,
                headers=self.headers,
                json=data,
                timeout=10
            ) as response:
                response.raise_for_status()
                return await response.json()
        except Exception as e:
            _LOGGER.error(f"API request failed: {str(e)}")
            raise

    async def get_devices(self):
        """Get all devices from Django server"""
        return await self._request('GET', 'api/devices/')

    async def get_device_state(self, device_id):
        """Get current state of specific device"""
        return await self._request('GET', f'api/devices/{device_id}/state/')

    async def update_device_state(self, device_id, state_data):
        """Update device state on server"""
        return await self._request('PUT', f'api/devices/{device_id}/state/', state_data)

    async def subscribe_to_updates(self, callback):
        """Subscribe to device state updates"""
        # This would use WebSocket in real implementation
        pass

    async def close(self):
        """Close the session"""
        await self.session.close()