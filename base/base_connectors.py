from utils.config import user,host,port,password,database
import psycopg2
from psycopg2 import Error


def test_connection():
    try:
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user=user,
                                      # пароль, который указали при установке PostgreSQL
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        cursor = connection.cursor()
        print("Информация о сервере PostgreSQL")
        print(connection.get_dsn_parameters(), "\n")
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")


def insert_to_base(insert_query):
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
        cursor = connection.cursor()
        cursor.execute(insert_query)
        connection.commit()
        print("[INFO] успешно: ", insert_query)
        mistake = False
    except (Exception, Error) as error:
        print("[INFO] Ошибка при работе с PostgreSQL", error)
        mistake = error
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
    return mistake

def insert_and_get_from_base(insert_query):
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
        cursor = connection.cursor()
        cursor.execute(insert_query)
        record = cursor.fetchall()
        connection.commit()
        print("[INFO] успешно: ", insert_query)
    except (Exception, Error) as error:
        print("[INFO] Ошибка при работе с PostgreSQL", error)
        record = None
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
    return record



def get_from_base(insert_query):
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
        cursor = connection.cursor()
        cursor.execute(insert_query)
        record = cursor.fetchall()
        print("[INFO] Успешно", insert_query)
        print("[INFO] Вернулось: ", record)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")
        return record


def get_messages_from_base_last_5(user_id):
    query = f"SELECT is_answer, message_body FROM messages WHERE storage_id = {user_id} ORDER BY id DESC LIMIT 5;"
    bd_messages = get_from_base(query)
    return bd_messages

def get_target_message(user_id: int):
    query = f"SELECT message_id FROM users WHERE user_id = {user_id}"
    answer = get_from_base(query)
    return answer
