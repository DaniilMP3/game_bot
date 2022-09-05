from create_bot import dp
from aiogram import executor
from guess_word import register_croco_handlers
from anagrams import register_anagrams_handlers
from send_to_chat import register_send_handler
from statistics import register_stats_handler
from sticks import register_sticks_handlers
from start import register_start_handler
from month_game import register_months_handlers


async def on_startup(_):
    print('Online')
    register_send_handler(dp)
    register_croco_handlers(dp)
    register_anagrams_handlers(dp)
    register_stats_handler(dp)
    register_months_handlers(dp)
    register_sticks_handlers(dp)
    register_start_handler(dp)


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)






