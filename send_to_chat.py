from aiogram import types, Dispatcher
from create_bot import bot
from custom_filters import IsDanik


async def send_to_chat(message: types.Message):
    if message.chat.type == 'private' and message.from_user.id == 879794827:
        await bot.send_message(-1001711898111, message.text)


def register_send_handler(dp: Dispatcher):
    dp.register_message_handler(send_to_chat, IsDanik())