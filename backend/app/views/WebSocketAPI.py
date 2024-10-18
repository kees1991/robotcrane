from starlette.websockets import WebSocket
from typing import List


class WebSocketAPI:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

        print(f"Connected")

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

        print(f"Disconnected")

    async def receive_message(self, websocket: WebSocket) -> str:
        return await websocket.receive_text()

    async def send_message(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)
