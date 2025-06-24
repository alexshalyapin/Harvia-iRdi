# websocket.py - обработка WebSocket соединений
import json
import logging
import asyncio
import websockets
from typing import Callable

_LOGGER = logging.getLogger('harvia_sauna')

class HarviaWebSocketClient:
    def __init__(self, url, token):
        self.url = url
        self.token = token
        self.connection = None
        self.subscribers = []
        self.reconnect_delay = 5
        self._running = False

    async def connect(self):
        """Connect to WebSocket server"""
        self._running = True
        while self._running:
            try:
                headers = {'Authorization': f'Token {self.token}'}
                async with websockets.connect(
                    self.url,
                    extra_headers=headers
                ) as self.connection:
                    _LOGGER.info("WebSocket connected")
                    await self._listen()
            except Exception as e:
                _LOGGER.error(f"WebSocket error: {str(e)}")
                await asyncio.sleep(self.reconnect_delay)

    async def _listen(self):
        """Listen for incoming messages"""
        async for message in self.connection:
            try:
                data = json.loads(message)
                await self._handle_message(data)
            except Exception as e:
                _LOGGER.error(f"Message handling error: {str(e)}")

    async def _handle_message(self, data):
        """Handle incoming WebSocket message"""
        _LOGGER.debug(f"Received WebSocket message: {data}")
        for callback in self.subscribers:
            try:
                await callback(data)
            except Exception as e:
                _LOGGER.error(f"Callback error: {str(e)}")

    def subscribe(self, callback: Callable):
        """Subscribe to state updates"""
        self.subscribers.append(callback)

    async def disconnect(self):
        """Disconnect from WebSocket"""
        self._running = False
        if self.connection:
            await self.connection.close()