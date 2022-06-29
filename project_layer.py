from setup import bot, dp
from aiogram import executor, Bot, Dispatcher, types, exceptions
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@dp.message_handlers(command=['start'])
async def start(message: types.Message):
    await message.reply("aboba")
    