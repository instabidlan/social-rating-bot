from logic_layer import *
from os import environ
from aiogram import executor, Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=environ["BOT_TOKEN"])
dp = Dispatcher(bot)
storage = MemoryStorage()


async def anti_flood(*args, **kwargs):
    m = args[0]
    change_social_rating(m.from_user.id, m.from_user.username, -200)
    await m.answer("Партия не любит спамеров!!! -200 social credit")


@dp.message_handler(commands=['social'])
async def social(message: types.Message):
    await message.delete()
    output = stats_func_output(
        user_id=message.from_user.id,
        username=message.from_user.username
    )

    await bot.send_message(
        text=output,
        chat_id=message.chat.id,
        parse_mode="MarkdownV2")


@dp.throttled(anti_flood, rate=3)
@dp.message_handler()
async def chat_msg_handler(message: types.Message):
    pass


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
