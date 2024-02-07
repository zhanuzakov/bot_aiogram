from aiogram import types, Router, Bot, F
from aiogram.filters import CommandStart, Command
import sqlite3
from google.cloud import vision
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"schoolbot-413405-2b1b7cbca3de.json"
TOKEN_API = "6518664848:AAFIqOgQAgtRPylMugzSMvH0vQI8-IvCPho"

bot = Bot(TOKEN_API)
client = vision.ImageAnnotatorClient()
user_private_router = Router()
@user_private_router.message(CommandStart())
async def start(message: types.Message):
    conn = sqlite3.connect('scores.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS scores (user_id INTEGER PRIMARY KEY, score INTEGER DEFAULT 0)')
    conn.commit()
    cur.close()
    conn.close()

@user_private_router.message(Command('scoreboard'))
async def scoreboard(message: types.Message):
    conn = sqlite3.connect('scores.db')
    cur = conn.cursor()
    cur.execute("SELECT user_id, score FROM scores ORDER BY score DESC")
    scores = cur.fetchall()
    conn.close()

    if scores:
        scoreboard_text = "Таблица лидеров:\n"
        for user_id, score in scores:
            user = bot.get_chat(user_id)
            username = user.username if user.username else user.first_name
            scoreboard_text += f"{username}: {score}\n"
    else:
        scoreboard_text = "Таблица лидеров пуста."
    await message.answer(scoreboard_text)

@user_private_router.message(Command('tasks'))
async def tasks(message: types.Message):
    task_list = await generate_task_list()
    task_text = "Список задач:\n"
    for i, task in enumerate(task_list, 1):
        task_text += f"{i}. {task}\n"
    await message.answer(task_text)

async def generate_task_list():
    tasks = [
        "Кошка",
        "Ноутбук",
        "Ручка",
        "Автомобиль",
        "Дерево",
        "Жилой комплекс",
        "Стадион",
        "Велосипед",
        "Слон",
        "Очки"
    ]
    return tasks

@user_private_router.message(F.photo)
async def handle_photos(message: types.Message):
    photo_file = await bot.get_file(message.photo[-1].file_id)
    file_path = photo_file.file_path

    photo_bytes = await bot.download_file(file_path)
    image = vision.Image(content=photo_bytes.getvalue())

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if labels:
        highest_score_label = labels[0].description  # Первый элемент имеет наивысший score
        await message.reply(f"{highest_score_label}")
    else:
        await message.reply("Не удалось определить содержимое изображения.")