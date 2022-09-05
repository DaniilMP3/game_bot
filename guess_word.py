from create_bot import bot, dp, words, session
from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import time
from custom_filters import IsCroco
from statistics import main_stats_method
from game_operations import generate_word, start_game, stop_game


async def start_croco(message: types.Message):
    await start_game(message, 'croco')


async def show_or_generate_word(callback: types.CallbackQuery):
    chat_id = str(callback.message.chat.id)
    if not session[chat_id]:
        await bot.send_message(chat_id, "Вы сейчас не играете в крокодила.")
    else:
        if callback.from_user.id != session[chat_id]['game_leader']:
            await callback.answer("Вы не ведущий", show_alert=True)
        else:
            action = callback.data
            if action == 'usercheck':
                await callback.answer(f"Ваше слово: {session[chat_id]['word']}", show_alert=True)
            elif action == 'nextword':
                new_word = await generate_word()
                session[chat_id]['word'] = new_word
                await callback.answer(f'Ваше новое слово: {new_word}.', show_alert=True)


async def check_right_answers(message: types.Message):
    chat_id = str(message.chat.id)
    if message.from_user.id != session[chat_id]['game_leader']:
        right_word = session[chat_id]['word'].lower()
        if message.text.lower() == right_word:
            winner = str(message.from_user.first_name)
            await main_stats_method(chat_id, winner, session[chat_id]['status'])
            await bot.send_message(message.chat.id, f"Игрок {winner} угадал! Он становится ведущим.")
            session[chat_id]['word'] = await generate_word()
            session[chat_id]['game_leader'] = message.from_user.id
            await bot.send_message(message.chat.id, f'{message.from_user.first_name} объясняет слово!',
                                   reply_markup=InlineKeyboardMarkup(resize_keyboard=True).add(
                                       InlineKeyboardButton('Смотреть слово', callback_data=f'usercheck'),
                                       InlineKeyboardButton('Следующее слово', callback_data=f'nextword')
                                   ))


async def stop_croco(message: types.Message):
    await stop_game(message, 'croco')


def register_croco_handlers(dp: Dispatcher):
    dp.register_message_handler(start_croco, commands=['croco'],
                                chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
    dp.register_message_handler(stop_croco, commands=['stop_croco'],
                                chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
    dp.register_callback_query_handler(show_or_generate_word, Text(equals=['usercheck', 'nextword']), state=None)
    dp.register_message_handler(check_right_answers, IsCroco(), chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])



