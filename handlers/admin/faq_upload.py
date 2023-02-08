﻿from aiogram import Dispatcher, types
from aiogram.types import ParseMode, Message, ReplyKeyboardRemove, CallbackQuery
from create_bot import bot
from utils.config import ADMINS
from utils.statemachine import Admin
from aiogram.dispatcher import FSMContext

def get_keyboard_admin():
    buttons = [
        types.InlineKeyboardButton(text="ДобавитьFAQ", callback_data="faq_admin"),
        types.InlineKeyboardButton(text="БыстроОтветы", callback_data="fast_answers_menu_admin")]
    keyword = types.InlineKeyboardMarkup(row_width=1)
    keyword.add(*buttons)
    return keyword



async def welcome_to_admin_mode(message: types.Message,state:FSMContext):
    await state.finish()
    if message.from_user.id in ADMINS:
        await bot.send_message(message.from_user.id, f"Вы в admin mode\n"
                                                     f"Для выхода введите /start\n",
                               reply_markup=get_keyboard_admin())
        await Admin.admin.set()
    else:
        await bot.send_message(message.from_user.id,'Отказано в доступе')


async def faq_refactor_mode(callback_query: CallbackQuery,):
    await callback_query.answer("FAQ")
    await bot.send_message(callback_query.from_user.id,"Добавьте сообщение для изменения FAQ:")
    await Admin.faq_refactoring.set()



async def catch_faq(message: Message):
    text = message.html_text
    string = text.split("\n")[0].lower()
    if "3 вариант" in string:
        variant = "faq_3"
    elif "2 вариант" in string:
        variant = "faq_2"
    elif "1 вариант" in string:
        variant = "faq_1"
    else:
        variant = "Вариант не индефицирован." \
                  "Бот пытается найти в сообщении следующие ключевые слова '1 вариант', '2 вариант', '3 вариант'" \
                  "И сейчас, он их не нашёл. Или чего-то сломалось("
        await message.answer(variant)
        return
    print(variant)
    await message.answer(f"Сохраню как вариант {variant}")
    await bot.send_message(message.from_user.id, variant)
    with open("storages"+variant+".html", "w+", ) as fi:
        fi.write(text)
        fi.close()
        await message.answer("text is uploaded")
        await message.answer(f"для возврата нажмите /start \n"
                             f"или шлите следующий FAQ")


def register_handlers_upload_faq(dp: Dispatcher):
    dp.register_callback_query_handler(faq_refactor_mode, lambda c: c.data in ('faq_admin'), state = Admin.admin)
    dp.register_message_handler(welcome_to_admin_mode, commands=['admin'], state="*")
    dp.register_message_handler(catch_faq, state=Admin.faq_refactoring)
