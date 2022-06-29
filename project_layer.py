import asyncio

import aiogram
from logic_layer import *
from os import environ
from aiogram import executor, Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


bot = Bot(token=environ["BOT_TOKEN"])
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class LastMessage(StatesGroup):
    last_messages = State()


@dp.message_handler(commands=['social'])
async def social(message: types.Message):
    await message.delete()
    output = OutputLogic.stats_func_output(
        user_id=message.from_user.id,
        username=message.from_user.username
    )

    await bot.send_message(
        text=output,
        chat_id=message.chat.id,
        parse_mode="MarkdownV2")


@dp.message_handler(commands=['blacklist'])
async def blacklist(message: types.Message):
    await message.delete()

    await message.answer(OutputLogic.blacklist_helper(message.from_user.username), parse_mode="MarkdownV2")


@dp.message_handler(content_types=aiogram.types.ContentType.all())
@dp.message_handler(state=LastMessage.last_messages)
async def chat_msg_handler(message: types.Message, state):
    async with state.proxy() as data:
        AntispamLogic.antispam(message, data)

        if len(data['last_messages']) > 2:
            m = await message.answer('*Малафья с яйца, партия недовольна!!!!* спамить низя!!!! -50 social credit',
                                     parse_mode="MarkdownV2")
            SRLogic.change_social_rating(message.from_user.id, message.from_user.username, -50)
            await message.delete()
            await asyncio.sleep(5)
            await m.delete()

    print(storage.data)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
