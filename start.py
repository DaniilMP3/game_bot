from aiogram import types, Dispatcher
from create_bot import bot, session




async def start_command(message: types.Message):
    chat_id = message.chat.id
    session[chat_id] = {}
    await bot.send_message(chat_id, "Приветствую, игроки. Чтобы начать играть - выдайте боту права администратора."
                                                " Правила для всех игр можно узнать при помощи команды /help. Статистика по команде - /stats.\n"
                                                " Доступные игры:\n1.Крокодил - /croco\n2.Анаграммы - /anagrams\n3.Палочки - /sticks. \nУдачной игры:).")


def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'],
                                chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
