import asyncio
from aiogram import Bot, Dispatcher, types, Router

from SaveMessagesMiddleware import SaveMessagesMiddleware
from handlers.user_private import user_private_router

TOKEN_API = "6518664848:AAFIqOgQAgtRPylMugzSMvH0vQI8-IvCPho"
bot = Bot(TOKEN_API)
dp = Dispatcher()

dp.message.middleware(SaveMessagesMiddleware())
dp.include_router(user_private_router)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())

