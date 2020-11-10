from service.util.websocket import manager as manager
from service.core.config import CLIENT_SESSION, CLIENT_API_ID, CLIENT_API_HASH
from telethon import TelegramClient, events

# import logging

# logging.basicConfig(level=logging.WARNING)

# google translator
from googletrans import Translator

translator = Translator()

client = TelegramClient(CLIENT_SESSION, CLIENT_API_ID, CLIENT_API_HASH)


@client.on(events.NewMessage)
# This is our update handler. It is called when a new update arrives.
async def handler(event):

    sender = await event.get_sender()

    message = event.message.message

    if translator.detect(message).lang == "zh-CN":
        message = translator.translate(message, dest="ru").text

    data = {
        "first_name": sender.first_name,
        "last_name": sender.last_name,
        "username": sender.username,
        "from_id": event.from_id,
        "to_id": event.to_id.user_id,
        "content": message,
        "status": 0,
        "created_at": event.message.date,
    }

    # print(data)

    data = await manager.update(data)

    await manager.broadcast([data])
