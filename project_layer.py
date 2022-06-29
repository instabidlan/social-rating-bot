from config import TOKEN

from aiogram import executor, Bot, Dispatcher, types, exceptions
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handlers(command=['start'])
async def start(message: types.Message):
    await message.reply("aboba")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
