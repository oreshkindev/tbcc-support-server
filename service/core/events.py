from typing import Callable
from fastapi import FastAPI
from service.db.database import database
from service.util.telegram_client import client


def start_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        await database.connect()

        # Run the client until Ctrl+C is pressed, or the client disconnects
        await client.start()

    return start_app


def stop_handler(app: FastAPI) -> Callable:  # type: ignore
    async def stop_app() -> None:
        await database.disconnect()

    return stop_app
