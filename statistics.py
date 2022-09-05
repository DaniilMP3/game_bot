import json
from aiogram import types, Dispatcher
from create_bot import AVAILABLE_GAMES, bot


async def check_if_chat_has_stats(chat_id, data):
    if chat_id not in data:
        data[chat_id] = {}


async def check_if_chat_has_game(chat_id, game, data):
    if game not in data[chat_id]:
        data[chat_id][game] = {}


async def check_if_user_in_stats(chat_id, nickname, game, data):
    if nickname not in data[chat_id][game]:
        data[chat_id][game][nickname] = 0


async def write(chat_id, nickname, data, game):

    user_score_str = data[chat_id][game][nickname]
    user_score_int = int(user_score_str) + 1
    data[chat_id][game][nickname] = str(user_score_int)
    with open('stats.json', 'w') as file:
        json.dump(data, file)


async def main_stats_method(chat_id, nickname, game):
    with open('stats.json') as file:
        data = json.load(file)
    await check_if_chat_has_stats(chat_id, data)
    await check_if_chat_has_game(chat_id, game, data)
    await check_if_user_in_stats(chat_id, nickname, game, data)
    await write(chat_id, nickname, data, game)


async def construct_string(chat_id, data, game):
    string = f'\n\nЛучшие игроки в {AVAILABLE_GAMES[game]}:'
    sort_rating = {k: v for k, v in sorted(data[chat_id][game].items(), key=lambda item: int(item[1]), reverse=True)}
    for user in sort_rating:
        string += f'\n{user} - {sort_rating[user]}.'
    return string


async def show_stats(message: types.Message):
    chat_id = str(message.chat.id)
    with open('stats.json') as file:
        data = json.load(file)
    str_to_send = 'Статистика:\n'

    if chat_id in data:
        cur_chat_played_games = data[chat_id].keys()
        for game in cur_chat_played_games:
            str_to_send += await construct_string(chat_id,
                                                  data, game)
        await bot.send_message(chat_id, str_to_send)
    else:
        await bot.send_message(chat_id, "Вы ещё не играли в игры.")


def register_stats_handler(dp: Dispatcher):
    dp.register_message_handler(show_stats, commands=['stats'],
                                chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])





