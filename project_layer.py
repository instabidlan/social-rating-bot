from logic_layer import *
from os import environ
from aiogram import executor, Bot, Dispatcher, types


bot = Bot(token=environ["BOT_TOKEN"])
dp = Dispatcher(bot)


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


@dp.message_handler()
async def chat_msg_handler(message: types.Message):
    decision = make_decision(
        user_id=message.from_user.id,
        username=message.from_user.username
    )
    if decision:
        await message.reply(text=decision)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
