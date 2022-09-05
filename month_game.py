from aiogram.types import Message, CallbackQuery, ChatType
from aiogram import Dispatcher
from create_bot import session, bot, dp

from game_operations import start_game, stop_game, add_in_lobby
from statistics import main_stats_method
from custom_filters import IsMonths
from aiogram.dispatcher.filters import Text


async def check_winner_change_date_and_move(chat_id, user_month, user_day, cur_game_move):
    if user_month == 'dec' and user_day == 31:
        winner = ' '.join([k for k, v in session[chat_id]['players'].items() if v == cur_game_move])
        await main_stats_method(chat_id, winner, session[chat_id]['status'])
        await bot.send_message(chat_id, f"Игрок {winner} победил! Игра окончена.")
        session[chat_id]['status'] = ''
    else:
        session[chat_id]['cur_month'] = user_month
        session[chat_id]['cur_day'] = user_day

        await bot.send_message(chat_id, f'Текущая дата - {session[chat_id]["cur_month"].capitalize()} {session[chat_id]["cur_day"]}.')

        next_player = ' '.join([k for k, v in session[chat_id]['players'].items() if v != cur_game_move])
        next_game_move = session[chat_id]['players'][next_player]
        session[chat_id]['cur_move'] = next_game_move

        await bot.send_message(chat_id ,f'Следующий ход игрока - {next_player}.')



async def start_months(message: Message):
    await start_game(message, 'months')


async def add_user_in_game(callback: CallbackQuery):
    chat_id = str(callback.message.chat.id)
    if session[chat_id]['months']['feb'][1] != 29:
        await add_in_lobby(callback, "Текущая дата - Jan 1.", additional_text="Этот год - не высокосный.")
    else:
        await add_in_lobby(callback, "Текущая дата - Jan 1." , additional_text='Этот год - высокосный.')


@dp.throttled(rate=2)
async def months_progress(message: Message):
    chat_id = str(message.chat.id)
    if len(session[chat_id]['players'].keys()) != 2:
        ###MESSAGES BEFORE GAME###
        pass
    else:
        player_move = session[chat_id]['players'][f'{message.from_user.first_name}']
        cur_game_move = session[chat_id]['cur_move']
        if player_move != cur_game_move:
            await bot.send_message(chat_id, f"{message.from_user.first_name}, сейчас не ваш ход.")

        else:
            user_date = message.text.split(' ')
            if len(user_date) != 2:
                await bot.send_message(chat_id, "Неверный формат.")
            else:
                user_month = user_date[0].lower()
                user_day = user_date[1]

                if user_month.lower() not in session[chat_id]['months'] or not user_day.isdigit() or user_day == '0':
                    await bot.send_message(chat_id, 'Дата введена неправильно.')
                else:
                    cur_month = session[chat_id]['cur_month']
                    cur_day = session[chat_id]['cur_day']
                    ###month info   0 - graduation 1 - days###
                    cur_month_info = session[chat_id]['months'][cur_month]
                    user_month_info = session[chat_id]['months'][user_month]

                    user_day = int(user_day)
                    if user_day > user_month_info[1]:
                        await bot.send_message(chat_id, 'В этом месяце нет столько дней.')
                    else:
                        if user_day < cur_day:
                            if user_month_info[0] < cur_month_info[0]:
                                await bot.send_message(chat_id, 'Вы ввели дату, которая была в прошлом.')
                            elif user_month_info[0] > cur_month_info[0]:
                                await bot.send_message(chat_id, 'Вы изменили месяц и дату.')
                            else:
                                await bot.send_message(chat_id, 'Вы ввели число, которое было в прошлом.')

                        elif user_day > cur_day:
                            if user_month_info[0] < cur_month_info[0]:
                                await bot.send_message(chat_id, 'Вы ввели дату, которая была в прошлом.')
                            elif user_month_info[0] > cur_month_info[0]:
                                await bot.send_message(chat_id, 'Вы изменили месяц и дату.')
                            else:
                                await check_winner_change_date_and_move(chat_id, user_month, user_day, cur_game_move)
                        else:
                            if user_month_info[0] < cur_month_info[0]:
                                await bot.send_message(chat_id, 'Вы ввели дату, которая была в прошлом.')
                            elif user_month_info[0] == cur_month_info[0]:
                                await bot.send_message(chat_id, 'Вы ввели ту же дату.')
                            else:
                                await check_winner_change_date_and_move(chat_id, user_month, user_day, cur_game_move)

async def stop_months(message: Message):
    await stop_game(message, 'months')


def register_months_handlers(dp: Dispatcher):
    dp.register_message_handler(start_months, commands=['months'],
                                chat_type=[ChatType.SUPERGROUP, ChatType.GROUP])
    dp.register_callback_query_handler(add_user_in_game, Text(startswith='months_'),
                                       chat_type=[ChatType.SUPERGROUP, ChatType.GROUP])
    dp.register_message_handler(months_progress, IsMonths(),
                                chat_type=[ChatType.SUPERGROUP, ChatType.GROUP]),
    dp.register_message_handler(stop_months, commands=['stop_months'],
                                chat_type=[ChatType.SUPERGROUP, ChatType.GROUP])






