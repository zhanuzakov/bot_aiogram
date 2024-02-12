from aiogram import BaseMiddleware
from pymongo import MongoClient
from typing import Callable, Awaitable
from aiogram import types

class SaveMessagesMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()

        # Настройка подключения к MongoDB
        self.client = MongoClient("mongodb+srv://alizhanuzak77:12345@cluster0.dydag3c.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['SchoolBotDB']
        self.messages_collection = self.db['BotUsers']

    async def __call__(
            self,
            handler: Callable[[types.Message, dict], Awaitable[None]],
            event: types.Message,
            data: dict
    ) -> None:
        # Сохраняем все сообщения в MongoDB
        self.messages_collection.insert_one({
            "user_id": event.from_user.id,
            "message_id": event.message_id,
            "text": event.text,
            "date": event.date.isoformat()
        })

        # Передаем управление следующему в цепочке обработчику
        await handler(event, data)
