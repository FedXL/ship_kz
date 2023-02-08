from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, ParseMode
import aiogram.utils.markdown as md
import datetime
from base.base_connectors import insert_and_get_from_base
from base.base_handlers_bot import add_user_to_base
from create_bot import bot
from handlers.chat.sender import catch_messaging
from sheets.add_orders import add_last_string

from utils.config import orders_chat_storage
from utils.markap_menu import SuperMenu
from utils.texts import make_user_info_report, order_answer_vocabulary, get_additional_from_proxi
from utils.utils_lite import create_new_message_order, quot_replacer


async def make_order_answer(query: CallbackQuery, state: FSMContext):
    await query.answer("Успешно")
    await query.message.delete_reply_markup()
    await query.message.delete()
    income = query.data
    match income:
        case "KAZ_ORDER_LINKS":
            async with state.proxy() as data:
                try:
                    addition = get_additional_from_proxi(data)
                except:
                    addition = "ERROR"
                    print(data)
        case "KAZ_ORDER_CABINET":
            async with state.proxy() as data:
                addition = [
                    md.text('Магазин: ', f"<code>{data.get('shop')}</code>"),
                    md.text('Логин: ', f"<code>{data.get('log')}</code>"),
                    md.text('Пароль: ', f"<code>{data.get('pass')}</code>"),
                ]
        case "TRADEINN":
            async with state.proxy() as data:
                addition = [
                    md.text('Логин: ', f"<code>{data.get('login')}</code>"),
                    md.text("Пaроль: ", f"<code>{data.get('pass')}</code>")
                ]
        case "PAYMENT":
            async with state.proxy() as data:
                addition = [
                    md.text('Магазин: ', f"<code>{data.get('shop')}</code>"),
                    md.text('Логин: ', f"<code>{data.get('login')}</code>"),
                    md.text('Пароль: ', f"<code>{data.get('pass')}</code>"),
                ]



    await state.finish()
    new_str = quot_replacer(str(addition))
    print("$" * 100, query.from_user.id, income, new_str, sep="\n")
    add_user_to_base(query.from_user.id,
                     income,
                     query.from_user.first_name,
                     query.from_user.last_name,
                     query.from_user.username)




    try:
        value = f"INSERT INTO orders (client,type,body,time) VALUES ({query.from_user.id},'{income}','{new_str}', NOW()) RETURNING id;"
        order_id = insert_and_get_from_base(value)[0][0]
        new_message = create_new_message_order(query, income, order_id)

        await catch_messaging(new_message)

    except Exception as er:
        order_id = None
        print("[ERROR] ", value)
        print("[ERROR] ORDER didnt was SAVED IN save_orders.orders_callback 52 string",er)
    user_info = make_user_info_report(query, order_id)
    pre_additional = order_answer_vocabulary(income, order_id)



    await bot.send_message(query.from_user.id, md.text(
        md.text("Уважаемый", query.from_user.username, "!", sep=" "),
        md.text("Мы получили ваш заказ:"),
        sep="\n"))

    await bot.send_message(query.from_user.id, md.text(
        md.text(*pre_additional, sep="\n"),
        md.text(*addition, sep="\n"),
        sep="\n"),
                           reply_markup=SuperMenu.cancel,
                           disable_web_page_preview=True,
                           parse_mode=ParseMode.HTML)

    await bot.send_message(query.from_user.id, md.text("Ваш заказ будет обработан сегодня.",
                                                       "Скоро с вами свяжется наш специалист.", "@ShipKZ",
                                                       sep="\n"))

    await bot.send_message(orders_chat_storage,
                           md.text(md.text(user_info),
                                   md.text(*addition, sep="\n"),
                                   sep="\n"),
                           disable_web_page_preview=True,
                           parse_mode=ParseMode.HTML)
    try:
        await add_last_string([(order_id, query.from_user.id, str(datetime.datetime.now()), income, new_str)], 'orders_storage')
        if income in ['KAZ_ORDER_LINKS', 'KAZ_ORDER_CABINET','PAYMENT']:
            await add_last_string([(order_id, query.from_user.id, str(datetime.date.today()), income, new_str)], 'Dashboard')
    except Exception as ER:
        print(f"[ERROR] google sheets error in orders callback: {ER}")

def register_handlers_save_order(dp: Dispatcher):
    dp.register_callback_query_handler(make_order_answer,
                                       lambda c: c.data in ['KAZ_ORDER_LINKS', 'KAZ_ORDER_CABINET', 'TRADEINN',
                                                            'PAYMENT'],
                                       state="*")
