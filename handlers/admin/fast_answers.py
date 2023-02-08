from aiogram import Dispatcher, types
from aiogram.types import ParseMode, Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from base.base_connectors import insert_to_base, get_from_base
from create_bot import bot
from utils.statemachine import Admin
from utils.utils_lite import quot_replacer


def get_keyboard_answers_menu():
    keyword = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text="Добавить ответ", callback_data="add_answer"),
        types.InlineKeyboardButton(text="🔽", callback_data="answers_expand")]
    keyword.add(*buttons)
    return keyword


def get_keyboard_comeback():
    keyword = types.InlineKeyboardMarkup(row_width=3)
    buttons = [
        types.InlineKeyboardButton(text="↪️", callback_data="answers_comeback")]
    keyword.add(*buttons)
    return keyword


def get_keyboard_refactor_answer():
    keyword = types.InlineKeyboardMarkup(row_width=3)
    buttons = [
        types.InlineKeyboardButton(text="удалить", callback_data=""),
        types.InlineKeyboardButton(text="поменять", callback_data=""),
        types.InlineKeyboardButton(text="↪️", callback_data="answers_comeback")]


def get_keyboard_answers_all():
    value = "SELECT id,body FROM fast_answers ORDER BY id;"
    query = get_from_base(value)
    keyword = types.InlineKeyboardMarkup(row_width=1)
    for id, body in query:
        if len(str(body)) > 45:
            text = str(body)[:45] + "..."
        else:
            text = str(body)
        button = InlineKeyboardButton(text=f"{id}. {text}", callback_data=f"{id}")
        keyword.add(button)
    keyword.add(types.InlineKeyboardButton(text="🔼", callback_data="fast_answers_menu_admin"))
    return keyword

def get_keyboard_answers_all_clean():
    value = "SELECT id,body FROM fast_answers ORDER BY id;"
    query = get_from_base(value)
    keyword = types.InlineKeyboardMarkup(row_width=1)
    count=1
    for id, body in query:
        if len(str(body)) > 45:
            text = str(body)[:45] + "..."
        else:
            text = str(body)
        if body != 'Null' and body != None:

            button = InlineKeyboardButton(text=f"{count}. {text}", callback_data=f"answer_{id}")
            keyword.add(button)
            count+=1

    keyword.add(types.InlineKeyboardButton(text="🔼", callback_data="fast_back"))
    return keyword




async def fast_answers_admin(callback_query: CallbackQuery):
    await callback_query.answer("Answer menu")
    await Admin.answers.set()
    await callback_query.message.edit_text("Вы в меню быстро-ответов", reply_markup=get_keyboard_answers_menu())


async def fast_answers_admin_expand(callback_query):
    await callback_query.answer("Answer menu")
    await callback_query.message.edit_text("Редактировать быстро-ответы", reply_markup=get_keyboard_answers_all())


async def add_answer(callback_query: CallbackQuery):
    await callback_query.answer("Добавить ответ")
    await bot.send_message(callback_query.from_user.id, "Введитете текст быстроответа:")
    await Admin.add_answer.set()


async def catch_answer(message: Message):
    print(message.content_type)
    text = message.text
    safe_text = quot_replacer(text)
    value5 = f"INSERT INTO fast_answers (body) VALUES ('{safe_text}');"
    mistake = insert_to_base(value5)
    if mistake:
        await bot.send_message(message.from_user.id, f"Что то пошлоне так : {mistake}")
    else:
        await bot.send_message(message.from_user.id, "Успешно. Введите следующий быстроответ или вернитесь в меню",
                               reply_markup=get_keyboard_comeback())


async def catch_changed_answer(message: Message, state: FSMContext):
    text = message.text
    safe_text = quot_replacer(text)
    async with state.proxy() as data:
        id = data.get('id')
    value = f"UPDATE fast_answers SET body = '{safe_text}' WHERE id = {id};"
    result = insert_to_base(value)
    if result:
        await bot.send_message(message.from_user.id, f"Неудачно что-то пошло не так: {result}")
    else:
        await bot.send_message(message.from_user.id, "Успешно", reply_markup=get_keyboard_answers_all())
        await Admin.answers.set()


async def catch_callback(callback_query: CallbackQuery, state: FSMContext):
    keyword = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(text="Удалить", callback_data="delete_answer"),
        types.InlineKeyboardButton(text="Поменять", callback_data="change_answer"),
        types.InlineKeyboardButton(text="↪️", callback_data="answers_comeback")]
    keyword.add(*buttons)

    await callback_query.answer(callback_query.data)
    id = callback_query.data
    value = f"SELECT body FROM fast_answers WHERE id = {id};"
    text = get_from_base(value)[0][0]

    await bot.send_message(callback_query.from_user.id, f"{id}. Ответ")
    await bot.send_message(callback_query.from_user.id, str(text))
    await bot.send_message(callback_query.from_user.id, "Удалить или Обновить желаете?", reply_markup=keyword)
    async with state.proxy() as data:
        data['id'] = id
    await Admin.change_answer.set()

async def answers_comeback(callback_query: CallbackQuery):
    await Admin.answers.set()
    await callback_query.answer("Answers menu")
    await bot.send_message(callback_query.from_user.id, "Вы в меню быстро-ответов",
                           reply_markup=get_keyboard_answers_all())
    await callback_query.message.delete()


async def start_change_answer(callback_query: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        id = data.get('id')
        print("id  ********************", id)
    match callback_query.data:
        case 'delete_answer':
            print("DELETE")
            value = f"UPDATE fast_answers SET body = 'Null' WHERE id = {id};"
            insert_to_base(value)
            await Admin.answers.set()
            await fast_answers_admin_expand(callback_query)
        case 'change_answer':
            print("CHANGE")
            await bot.send_message(callback_query.from_user.id, "Введите новый быстро-ответ:")
            await Admin.change_change_answer.set()
        case 'answers_comeback':
            print("COMEBACK")
            await Admin.answers.set()
            await fast_answers_admin_expand(callback_query)


def register_handlers_fast_answers(dp: Dispatcher):
    dp.register_callback_query_handler(fast_answers_admin,
                                       lambda c: c.data in ('fast_answers_menu_admin'),
                                       state=[Admin.admin, Admin.answers])

    dp.register_callback_query_handler(fast_answers_admin_expand,
                                       lambda c: c.data in ('answers_expand'),
                                       state=Admin.answers)

    dp.register_callback_query_handler(add_answer,
                                       lambda c: c.data in ('add_answer'),
                                       state=Admin.answers)

    dp.register_message_handler(catch_answer,
                                state=Admin.add_answer,
                                content_types=['text'])

    dp.register_callback_query_handler(answers_comeback,
                                       lambda c: c.data in ('answers_comeback'),
                                       state=[Admin.add_answer, Admin.answers])

    dp.register_callback_query_handler(catch_callback,
                                       state=Admin.answers)

    dp.register_callback_query_handler(start_change_answer,
                                       lambda c: c.data in ('delete_answer', 'change_answer', 'answers_comeback'),
                                       state=Admin.change_answer)

    dp.register_message_handler(catch_changed_answer, state=Admin.change_change_answer)
