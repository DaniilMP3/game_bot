from aiogram import types, Dispatcher
from create_bot import session, bot, dp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from custom_filters import IsSticks
from aiogram.dispatcher.filters import Text
from random import randint
from statistics import main_stats_method
import time
from game_operations import stop_game, start_game, add_in_lobby


async def start_sticks(message: types.Message):
    await start_game(message, 'sticks')


async def add_user_in_game(callback: types.CallbackQuery):
    chat_id = str(callback.message.chat.id)
    await add_in_lobby(callback, session[chat_id]['sticks'])


@dp.throttled(rate=2)
async def sticks_progress(message: types.Message):
    chat_id = str(message.chat.id)
    print(session)
    if len(session[chat_id]['players'].keys()) != 2:
        ###MESSAGES BEFORE GAME###
        pass
    else:
        player_move = session[chat_id]['players'][f'{message.from_user.first_name}']
        cur_game_move = session[chat_id]['cur_move']
        if player_move != cur_game_move:
            await bot.send_message(chat_id, f"{message.from_user.first_name} ,сейчас не ваш ход.")

        else:
            sticks_str = session[chat_id]['sticks']
            if message.text.isdigit():
                digit = int(message.text)
                if digit > 5:
                    await bot.send_message(chat_id, "Число больше чем 5!")
                elif len(sticks_str) - digit <= 0 or digit == 0:
                    await bot.send_message(chat_id, "Неверное число.")
                else:
                    new_sticks_str = sticks_str[0:len(sticks_str) - digit]
                    session[chat_id]['sticks'] = new_sticks_str
                    if len(new_sticks_str) == 1:
                        winner = ' '.join([k for k, v in session[chat_id]['players'].items() if v == player_move])
                        await main_stats_method(chat_id, winner, session[chat_id]['status'])
                        await bot.send_message(chat_id, f"Игрок {winner} победил! Игра окончена.")
                        session[chat_id]['status'] = ''
                    else:
                        await bot.send_message(chat_id ,f"Палочек осталось {len(new_sticks_str)}:\n{new_sticks_str}")
                        next_player = ' '.join([k for k, v in session[chat_id]['players'].items() if v != cur_game_move])
                        next_game_move = session[chat_id]['players'][next_player]
                        session[chat_id]['cur_move'] = next_game_move
                        await bot.send_message(chat_id, f"Следующий ход игрока - {next_player}.")
            else:
                await bot.send_message(chat_id, f"{message.from_user.first_name}, вы ввели не число.")


async def stop_sticks(message: types.Message):
    await stop_game(message, 'sticks')



def register_sticks_handlers(dp: Dispatcher):
    dp.register_message_handler(start_sticks, commands=['sticks'],
                                chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
    dp.register_callback_query_handler(add_user_in_game, Text(startswith='sticks_'),
                                       chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
    dp.register_message_handler(sticks_progress, IsSticks(),
                                chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP]),
    dp.register_message_handler(stop_sticks, commands=['stop_sticks'],
                                chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
