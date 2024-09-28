import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from config import token


dp = Dispatcher()
bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Добавил в список админов")


@dp.message(F.text.startswith("https://omarket"))
async def omarket_handler(message: types.Message) -> None:
    try:
        with open("links.txt", "a", encoding="utf-8") as f:
            f.write(message.text)
    except Exception as e:
        await message.answer("Something went wrong!")



async def start_bot() -> None:
    await dp.start_polling(bot)


