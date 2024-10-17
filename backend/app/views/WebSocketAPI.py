from starlette.websockets import WebSocket
from typing import List


class WebSocketAPI:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

        print(f"Connected")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

        print(f"Disconnected")

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
