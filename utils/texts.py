import random
import re
import aiogram.utils.markdown as md
from aiogram import types
from aiogram.types import CallbackQuery
from utils.utils_lite import create_counter


def make_text_hello(username):
    text_hello = md.text(
        md.text("🫱   Добро пожаловать,", "*",username ,"*","!","Я Бот-Помощник."),
        md.text(" "),
        md.text("🔸  Могу оформить заказ , в разделе 'Сделать заказ'."),
        md.text(""),
        md.text("🔸  Ответы на большинство вопросов и калькулятор стоимости в разделе 'Kонсультация'."),
        md.text(" "),
        md.text("🗣  В случае необходимости, и, если раздел консультаций не помог, для связи с живым консультантом просто пишите в чат. "),
        # md.text(" "),
        # md.text("🔸     Полное описание возможностей: /help"),
        # md.text("Полное описание моих возможностей /help "),
        sep="\n"
    )
    return text_hello





def make_text_for_FAQ(value: str):
    try:
        with open("storages" + value + ".html", "r", ) as fi:
            result = fi.read()
            fi.close()
    except Exception as ex:
        print("чето пошло не так")
    return result


def make_user_info_report(query: CallbackQuery, order_id=None) -> md.text():
    user_id = query.from_user.id
    user_first_name = query.from_user.first_name
    user_second_name = query.from_user.last_name
    username = query.from_user.username
    result = md.text(
        md.text(f" #{order_id}"),
        md.text(f"Type: <b>{query.data}</b>"),
        md.text(f"User: ", md.hlink(f"#ID_{user_id}", f"tg://user?id={user_id}")),
        md.text(f"First Name: {user_first_name}"),
        md.text(f"Second Name: {user_second_name}"),
        md.text(f"UserName :  @{username}"),
        sep="\n"
    )
    return result


def make_user_info_report_from_message(message: types.Message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_second_name = message.from_user.last_name
    username = message.from_user.username
    result = md.text(
        md.text(f"User:", md.hlink(f"#ID_{user_id}", f"tg://user?id={user_id}")),
        md.text(f"First Name: {user_first_name}"),
        md.text(f"Second Name: {user_second_name}"),
        md.text(f"UserName :  @{username}"),
        sep="\n"
    )
    return result


def make_mask_to_messages(income, user_id):
    assert isinstance(income, types.Message) or isinstance(income, types.CallbackQuery)

    user_first_name = income.from_user.first_name
    user_second_name = income.from_user.last_name
    username = income.from_user.username
    result = md.text(
        md.text(md.hlink(f"#ID_{user_id}", f"tg://user?id={user_id}")),
        md.text(f"{user_first_name}",
                f"{user_second_name}",
                f"@{username}", sep=" | "),
        sep="\n"
    )
    return result


def order_answer_vocabulary(income,order_id):
    if order_id:
        order_id+=100
    match income:
        case 'KAZ_ORDER_LINKS':
            text = ['Вариант 1', f'Заказ через Казахстан №{order_id}', 'ссылки']
        case 'KAZ_ORDER_CABINET':
            text = ['Вариант 1', f'Заказ через Казахстан №{order_id}', 'доступ в кабинет']
        case 'TRADEINN':
            text = ['Вариант 2', f'Заказ через TradeInn №{order_id}']
        case 'PAYMENT':
            text = ['Вариант 3', f'Выкуп через посредника №{order_id}']
    return text


def make_links_info_text(links):
    counter = create_counter()
    md_obj = [md.hlink("ссылка " + str(counter()), link) for link in links]
    return md_obj


def get_vaflalist(pos=1):
    if pos == 1:
        result = ('первая',
                  'вторая',
                  'третья',
                  'четвертая',
                  'пятая',
                  'шестая',
                  'седьмая',
                  'восьмая',
                  'девятая',
                  'десятая',
                  'одиннадцатая',
                  'двенадцатая',
                  'тринадцатая',
                  'четырнадцатая',
                  'пятнадцатая')
    elif pos == 2:
        result = ('первой',
                  'второй',
                  'третьей',
                  'четвертой',
                  'пятой',
                  'шестой',
                  'седьмой',
                  'восьмой',
                  'девятой',
                  'десятой',
                  'одиннадцатой',
                  'двенадцатой',
                  'тринадцатой',
                  'четырнадцатой',
                  'пятнадцатой',)
    return result


def get_additional_from_proxi(data):
    print("data "*10, data,sep="\n")
    addition = []
    hrefs = [data.get(key) for key in [('href_' + str(key)) for key in
                                       [i for i in range(1, data.get('num') + 1)]]]
    comments = [data.get(key) for key in
                [('comment_' + str(key)) for key in
                 [i for i in range(1, data.get('num') + 1)]]]
    link = iter(make_links_info_text(hrefs))
    comment = iter(comments)
    addition.append(md.text('shop: ', f"<code>{data['shop']}</code>"))
    for x in hrefs:
        new = md.text(next(link), ": ", f"{next(comment)}")
        addition.append(new)
    return addition


def get_id_from_text(text):
    id = re.search(r"#ID_(\d+)", text)
    if id:
        return id.group(1)
    else:
        return None


def make_message_text(message: list) -> md.text():

    result = []
    before = message[:1]
    after = message[1:]

    for is_answer, body in before:
        if is_answer:
            pointer = "✅"
            if len(body)>50:
                body = str(body[:50]) + "..."
        else:
            pointer = "🆘"

        result.append(md.text(pointer, body, sep=" "))
        result.append(md.text(" "))

    for is_answer, body in after:
        if is_answer:
            pointer = ''
        else:
            pointer = '👈'
        if len(str(body)) >= 80:
            insert_text = str(body)[:60] + "..."
        else:
            insert_text = str(body)

        result.append(md.text(pointer, insert_text, sep=" "))
    return result




def make_message_text_full(message: list) -> md.text():
    result = []
    before = message[:1]
    after = message[1:]

    for is_answer, body in before:
        if is_answer:
            pointer = "✅"
        else:
            pointer = "🆘"
        result.append(md.text(pointer, body, sep=" "))
        result.append(md.text(" "))
    for is_answer, body in after:
        if is_answer:
            pointer = ''
        else:
            pointer = '👈'
        result.append(md.text(pointer, body, sep=" "))
    return result
