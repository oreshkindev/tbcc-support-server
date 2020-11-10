from fastapi import WebSocket
import json
from fastapi.encoders import jsonable_encoder

from service.util import ticket as ticket
from service.schema.ticket import TicketModel


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, data: str):
        data = jsonable_encoder(data)
        for connection in self.connections:
            await connection.send_text(json.dumps(data))

    async def update(self, event):

        event = await ticket.create_ticket(TicketModel(**event))
        return event


manager = ConnectionManager()