from aiogram.dispatcher.filters import Filter
from create_bot import session, bot
from aiogram.types import Message, Update


class IsCroco(Filter):
    key = 'is_croco'

    async def check(self, message: Message):
        if message.text[0] != '/' and f"{message.chat.id}" in session:
            return session[f"{message.chat.id}"]['status'] == 'croco'



class IsAnagrams(Filter):
    key = 'is_anagrams'

    async def check(self, message: Message):
        if message.text[0] != '/' and f"{message.chat.id}" in session:
            return session[f"{message.chat.id}"]['status'] == 'anagrams'

class IsSticks(Filter):
    key = 'is_sticks'

    async def check(self, message: Message):
        user = message.from_user.first_name
        chat_id = str(message.chat.id)
        if message.text[0] != '/' and f"{message.chat.id}" in session and user in session[chat_id]['players']:
            return session[f"{message.chat.id}"]['status'] == 'sticks'

class IsMonths(Filter):
    key = 'is_months'

    async def check(self, message: Message):
        user = message.from_user.first_name
        chat_id = str(message.chat.id)
        if message.text[0] != '/' and f"{message.chat.id}" in session and user in session[chat_id]['players']:
            return session[f"{message.chat.id}"]['status'] == 'months'


class IsDanik(Filter):
    key = 'is_danik'

    async def check(self, message: Message):
        return message.from_user.id == 879794827 and message.chat.type == 'private'


