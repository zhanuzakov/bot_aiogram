from aiogram import types, Router, Bot, F
from aiogram.filters import CommandStart, Command
import sqlite3
from google.cloud import vision
import os
import asyncio
from aiogram import Bot, Dispatcher, types, Router


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"schoolbot-413405-2b1b7cbca3de.json"
TOKEN_API = "6518664848:AAFIqOgQAgtRPylMugzSMvH0vQI8-IvCPho"

bot = Bot(TOKEN_API)
client = vision.ImageAnnotatorClient()

dp = Dispatcher()

@dp.message()
async def message_handler(message: types.Message) -> None:
    await SendMessage(chat_id=message.from_user.id, text=message.text)