from create_bot import bot, session, dp
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from custom_filters import IsAnagrams
from statistics import main_stats_method

from game_operations import start_game, setStatus, get_right_word_and_shuffle, stop_game


async def start_anagrams(message: types.Message):
    await start_game(message, 'anagrams')


async def stop_anagrams(message: types.Message):
    await stop_game(message, 'anagrams')


@dp.throttled(rate=3)
async def next_anagram(callback: types.CallbackQuery):
    await callback.answer()
    chat_id = str(callback.message.chat.id)
    if not session[chat_id]:
        await bot.send_message(chat_id, "Вы сейчас не играете в анаграммы.")
    else:
        new_right_and_shuffled_word = await get_right_word_and_shuffle()
        session[chat_id]['word'] = new_right_and_shuffled_word[0]
        msg = await bot.send_message(chat_id, f"Ваша новая анаграмма:\n{new_right_and_shuffled_word[1]}\n", reply_markup=types.InlineKeyboardMarkup(resize_keyboard=True).add(
                                     types.InlineKeyboardButton("Следующая анаграмма", callback_data="next_anagram")))

        await bot.delete_message(chat_id, session[chat_id]['game_message'])
        session[chat_id]['game_message'] = str(msg['message_id'])


async def check_right_answers(message: types.Message):
    chat_id = str(message.chat.id)
    if message.text.lower() == session[chat_id]["word"].lower():
        winner_nickname = str(message.from_user.first_name)
        right_word = str(message.text)
        await main_stats_method(chat_id, winner_nickname, session[chat_id]['status'])
        await bot.delete_message(chat_id, session[chat_id]['game_message'])
        await bot.send_message(chat_id, f"Пользователь {winner_nickname} угадал!\nПравильное слово - {right_word.lower()}")
        await setStatus(message, game_type='anagrams')



def register_anagrams_handlers(dp: Dispatcher):
    dp.register_message_handler(start_anagrams, commands=['anagrams'],
                                chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP]),
    dp.register_message_handler(stop_anagrams, commands=['stop_anagrams'],
                                chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP]),
    dp.register_callback_query_handler(next_anagram, Text(equals=['next_anagram']),
                                chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
    dp.register_message_handler(check_right_answers, IsAnagrams(),
                                chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])



