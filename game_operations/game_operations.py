from create_bot import session
from create_bot import bot
from aiogram import types
from random import randint, shuffle
from time import time
from create_bot import words


async def generate_word():
    seed = int(time())
    rand_int = (seed * 134775813) % 4294967296
    return words[rand_int % len(words)]


async def get_right_word_and_shuffle():
    word = await generate_word()
    letters_to_shuffle = [letter.upper() for letter in word]
    shuffle(letters_to_shuffle)
    return [word, '.'.join(letters_to_shuffle)]


async def setStatus(message, game_type):
    chat_id = str(message.chat.id)
    session[chat_id] = {}
    if game_type == 'croco':
        msg = await bot.send_message(chat_id, f'{message.from_user.first_name} объясняет слово!',
                               reply_markup=types.InlineKeyboardMarkup(resize_keyboard=True).add(
                                   types.InlineKeyboardButton('Смотреть слово', callback_data=f'usercheck'),
                                   types.InlineKeyboardButton('Следующее слово', callback_data=f'nextword')))


        session[chat_id] = {'game_leader': message.from_user.id,
                            'word': await generate_word(),
                            'status': 'croco',
                            'game_message': str(msg['message_id'])}



    elif game_type == 'anagrams':
        right_and_shuffled_word = await get_right_word_and_shuffle()

        msg = await bot.send_message(chat_id, f"Угадайте анаграмму:\n{right_and_shuffled_word[1]}",
                                     reply_markup=types.InlineKeyboardMarkup(resize_keyboard=True).add(
                                     types.InlineKeyboardButton("Следующая анаграмма", callback_data="next_anagram")))

        session[chat_id] = {'word': right_and_shuffled_word[0],
                            'status': 'anagrams',
                            'game_message': str(msg['message_id'])}

    elif game_type == 'sticks':
        msg = await bot.send_message(chat_id, "Проводится набор игроков для игры в палочки:",
                               reply_markup=types.InlineKeyboardMarkup(resize_keyboard=True).add(
                               types.InlineKeyboardButton('Присоединится к игре', callback_data="sticks_")))
        session[chat_id] = {'status': 'sticks',
                            'players': {},
                            'main_message': message.message_id,
                            'sticks': '||||||||||||||||||||',
                            'cur_move': 'first',
                            'game_message': str(msg['message_id'])}

    elif game_type == 'months':

        msg = await bot.send_message(chat_id, "Проводится набор игроков для игры в месяца:",
                               reply_markup=types.InlineKeyboardMarkup(resize_keyboard=True).add(
                                   types.InlineKeyboardButton('Присоединится к игре', callback_data='months_')))

        session[chat_id] = {'status': 'months',
                            'players': {},
                            'cur_move': 'first',
                            'cur_month': 'jan',
                            'cur_day': 1,
                            'game_message': str(msg['message_id']),
                            'months': {
                                'jan': [1, 30],
                                'feb': [2, 28],
                                'mar': [3, 31],
                                'apr': [4, 30],
                                'may': [5, 31],
                                'jun': [6, 30],
                                'jul': [7, 31],
                                'aug': [8, 31],
                                'sep': [9, 30],
                                'oct': [10, 31],
                                'nov': [11, 30],
                                'dec': [12, 31]}}

        is_leap = randint(28, 29)
        if is_leap == 28:
            ###LEAVE PREVIOUS FEB DAYS VALUE###
            pass
        else:
            session[chat_id]['months']['feb'][1] = 29




async def start_game(message, game_type):
    chat_id = str(message.chat.id)
    if chat_id in session:
        if session[chat_id]['status'] != '':
            await bot.send_message(chat_id, 'Вы уже играете в какую-то игру.')
        else:
            await setStatus(message, game_type)
    else:
        await setStatus(message, game_type)


async def stop_game(message, game_type):
    chat_id = str(message.chat.id)
    if session[chat_id]['status'] == game_type:
        session[chat_id]['status'] = ''
        await bot.send_message(chat_id, 'Вы закончили игру.')
        await bot.delete_message(chat_id, session[chat_id]['game_message'])
    else:
        await bot.send_message(chat_id, 'Вы сейчас не играете в эту игру.')



async def toss_coin(chat_id, player1, player2):
    rand_num = int(randint(1, 2))
    if rand_num == 1:
        ### STAY ORDER AS BEFORE ###
        pass
    else:
        session[chat_id]['players'][player2] = 'first'
        session[chat_id]['players'][player1] = 'second'


async def add_in_lobby(callback, ending_text, additional_text=False):
    chat_id = str(callback.message.chat.id)
    user_name = str(callback.from_user.first_name)
    if user_name in session[chat_id]['players']:
        await callback.answer("Вы уже присоединились к игре", show_alert=True)
    elif len(session[chat_id]['players'].keys()) >= 2:
        await callback.answer("Участики уже набраны.", show_alert=True)

    elif len(session[chat_id]['players'].keys()) == 0:
        await callback.answer()
        session[chat_id]['players'][user_name] = 'first'
        await callback.message.answer(f"{user_name} присоединился к игре")

    else:
        await callback.answer()
        session[chat_id]['players'][user_name] = 'second'
        await callback.message.answer(f"{user_name} присоединился к игре. Набор участников окончен.")
        if additional_text:

            await bot.send_message(chat_id, additional_text)


        players = list(session[chat_id]['players'].keys())
        await toss_coin(chat_id, players[0], players[1])
        first_player = ' '.join([k for k, v in session[chat_id]['players'].items() if v == 'first'])
        session[chat_id]['cur_move'] = session[chat_id]['players'][first_player]
        await bot.send_message(chat_id, f'По результатам подброса монеты, первым начинает - {first_player}. \n' +
                                        ending_text)