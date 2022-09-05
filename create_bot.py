from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os


AVAILABLE_GAMES = {'anagrams': 'Анаграммы', 'croco': 'Крокодил', 'sticks': 'Палочки', 'months': 'Месяца'}

session = {}

with open('10000-russian-words.txt', 'r', encoding='utf-8') as f:
    words = f.read().splitlines()

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())



