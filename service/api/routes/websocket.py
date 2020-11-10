from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from service.util.websocket import manager
from service.util import ticket as ticket_util
from service.util.telegram_client import client
import json

# google translator
from googletrans import Translator

translator = Translator()

router = APIRouter()


@router.websocket_route("/")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    tickets = await ticket_util.get_tickets(page=1)

    data = jsonable_encoder(tickets)
    await websocket.send_text(json.dumps(data))
    try:
        while True:
            data = await websocket.receive_text()

            data = json.loads(data)

            data = await manager.update(data)

            await manager.broadcast([data])

            await client.send_message(
                int(data["to_id"]),
                translator.translate(data["content"], dest="zh-cn").text,
            )

    except WebSocketDisconnect:
        manager.disconnect(websocket)