import asyncio
from aiogram import types
from aiogram.types import CallbackQuery, User, ChatType, Message
from create_bot import bot
from utils.config import MANAGER


def ShopValid(text: str) -> bool:
    try:
        new_text = int(text)
        return False
    except ValueError:
        pass
    if len(text) > 150:
        return False
    return True


def create_counter():
    i = 0

    def func():
        nonlocal i
        i += 1
        return i

    return func


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


def quot_replacer(text):
    try:
        text = text.replace("'", "''")
    except Exception as ER:
        print(ER)
    return text


def create_new_message_order(query: CallbackQuery, texts, order_id):

    texts = texts + f" /order_{order_id}"
    new_message = Message(chat_id=query.message.chat.id, text=texts, chat=ChatType())
    new_message.chat.type = 'private'
    new_message.from_user = User(alias='from', base=User)
    new_message.from_user.id = query.from_user.id
    new_message.from_user.first_name = query.from_user.first_name
    new_message.from_user.last_name = query.from_user.last_name
    new_message.from_user.username = query.from_user.username
    new_message.chat.id = False
    return new_message

def create_new_message_change(query: CallbackQuery,user_id,query_set:list):
    manager = MANAGER.get(query.from_user.id)
    texts = f"Перенаправлено от {manager}"
    new_message = Message(chat_id=query.message.chat.id, text=texts, chat=ChatType())
    new_message.chat.type = 'private'
    new_message.from_user = User(alias='from', base=User)
    new_message.from_user.id = user_id
    new_message.from_user.first_name = query_set[0]
    new_message.from_user.last_name = query_set[1]
    new_message.from_user.username = query_set[2]
    new_message.chat.id = False
    return new_message






async def disappear_message_message_is_send(message: types.Message):
    # Send the message
    if message.chat.id:
        sent_message = await bot.send_message(message.chat.id, '🔸Ваше сообщение отправлено🔸')
        # Delete the message after 5 seconds
        await asyncio.sleep(4)
        await bot.delete_message(message.chat.id, sent_message.message_id)
