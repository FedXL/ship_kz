from aiogram import types, Dispatcher
from aiogram.dispatcher import filters
from aiogram.types import ParseMode, Message, ChatType, User
import aiogram.utils.markdown as md
from base.base_connectors import get_from_base, get_messages_from_base_last_5
from create_bot import bot
from handlers.chat.sender import get_keyboard
from utils.texts import make_message_text, make_mask_to_messages
from utils.utils_lite import disappear_message_message_is_send


async def photo_reloader(message: types.Message, regexp_command):
    print('[INFO] photo reloader start')
    message_id = regexp_command.group(1)
    try:
        value = f"SELECT file_id FROM photos WHERE message_id = {message_id};"
        photo = get_from_base(value)[0][0]
        await bot.send_photo(message.chat.id, photo)

    except Exception as ER:
        print(f'[ERROR] photo_reloader: {ER}')
        await bot.send_message(message.chat.id, 'Фотография не найдена')
    await bot.delete_message(message.chat.id, message.message_id)


async def document_reloader(message: types.Message, regexp_command):
    print('[INFO] document reloader start')
    message_id = regexp_command.group(1)
    print(message_id)
    try:
        value = f"SELECT document_id FROM documents WHERE message_id = {message_id};"
        document = get_from_base(value)[0][0]
        await bot.send_document(message.chat.id, document)
    except Exception as ER:
        print(f'[ERROR] document_reloader: {ER}')
        await bot.send_message(message.chat.id, 'Документ не найден')
    await bot.delete_message(message.chat.id, message.message_id)


async def order_reloader(message: types.Message, regexp_command):
    print("[INFO] order reloader start")
    order_id = regexp_command.group(1)
    print(order_id)
    query = None
    try:
        value = f"SELECT type,body FROM orders WHERE id = {order_id};"
        query = get_from_base(value)[0]
        query_set = query[1]
        name = query[0]
        query_set = query_set[1:-1].split(",")
        new_query = []
        new_query.append(f"Заказ № {order_id}")
        new_query.append(name)
        for i in query_set:
            a = i.strip().strip("'")
            new_query.append(a)
    except Exception as ER:
        print("[ERROR] ", ER)
        await bot.send_message(message.chat.id,f"Ошибка скорее заказа номер {order_id} нет в базе.\n из базы вернулось: {query}, \n ERROR: {ER}")
    print("FTF!!!!!!!!!!!!!!!!!!!!!!!!!!",message.chat.id,message.message_id)
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.chat.id, md.text(*new_query, sep='\n'), parse_mode=ParseMode.HTML)


async def init_conversation(message: types.Message, regexp_command):
    user_id = regexp_command.group(1)
    print("INFO order init conversation message", user_id)
    insert_get_info = f"SELECT user_name,tele_username,user_second_name FROM users WHERE user_id = {user_id}"
    user_info = get_from_base(insert_get_info)
    print(user_info)
    if user_info == []:
        await bot.send_message(message.chat.id, f"Такого пользователя {user_id} нет в базе данных")
        return
    else:
        user_info = user_info[0]
    message_list = get_messages_from_base_last_5(user_id)
    text = make_message_text(message_list)
    new_message = Message(chat_id=message.chat.id, chat=ChatType())
    new_message.from_user = User(alias='from', base=User)
    new_message.from_user.first_name = user_info[0]
    new_message.from_user.last_name = user_info[1]
    new_message.from_user.username = user_info[2]
    text_info = make_mask_to_messages(new_message, user_id)


    # ОТПРАВЛЯЕМ СООБЩЕНИЕ В ГРУППУ
    await bot.send_message(message.chat.id, md.text(
        text_info,
        md.text(*text, sep="\n"),
        sep="\n"),
                           parse_mode=ParseMode.HTML,
                           reply_markup=get_keyboard())


def register_reload_media(dp: Dispatcher):
    dp.register_message_handler(photo_reloader, filters.RegexpCommandsFilter(regexp_commands=['photo_([0-9]*)']))
    dp.register_message_handler(document_reloader, filters.RegexpCommandsFilter(regexp_commands=['doc_([0-9]*)']))
    dp.register_message_handler(order_reloader, filters.RegexpCommandsFilter(regexp_commands=['order_([0-9]*)']))
    dp.register_message_handler(init_conversation, filters.RegexpCommandsFilter(regexp_commands=['talk_([0-9]*)']))
