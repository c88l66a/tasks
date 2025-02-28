from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from Env_generation.environment_generation import *
from Logging_module import log_module
from create_bot import bot

import psycopg2


DATABASE_URL = f"postgresql://{rm_db_user}:{rm_db_password}@{rm_db_host}:{rm_db_port}/{rm_db_name}"
engine = psycopg2.connect(DATABASE_URL)

#  ==================================== Вывод логов о репликации =================================
async def get_repl_logs(message: types.message):
    await bot.send_document(chat_id=message.chat.id, document=open("/logs/postgresql.log", "rb"), caption=
                                    f"Результат выполнения команды в виде отчета (так как сообщение плохо маштабируется в телеграмме)")
    log_module.logger.info(f"CHAPTER : /get_repl_logs, TELEGRAM_ID : {message.from_user.id}")

# ================================ Вывод данных из таблицы emails ================================
async def get_emails(message: types.message):
    try:
        cursor = engine.cursor()
        cursor.execute('SELECT email FROM emails')
        result = cursor.fetchall() # вернуть все строки
        emails = "\n".join(email[0] for email in result) # преобразование из json в строки
        await message.answer(f"Email-адреса:\n{emails}")
        cursor.close() # закрываем курсор
    except psycopg2.errors:
        await message.answer("Ошибка")
    log_module.logger.info(f"CHAPTER : /get_emails, TELEGRAM_ID : {message.from_user.id}")

# ================================ Вывод данных из таблицы phone ================================
async def get_phone_numbers(message: types.message):
    try:
        cursor = engine.cursor()
        cursor.execute('SELECT phone_number FROM phones')
        result = cursor.fetchall()
        phones = "\n".join(email[0] for email in result)
        await message.answer(f"Номера телефонов:\n{phones}")
        cursor.close()
    except psycopg2.errors:
        await message.answer("Ошибка")
    log_module.logger.info(f"CHAPTER : /get_phone_numbers, TELEGRAM_ID : {message.from_user.id}")

# =========================== Запись Email-адресов в бд ===========================
async def write_emails(state):
    try:
        cursor = engine.cursor()
        async with state.proxy() as data:
            emails = data["email"].split("\n")
            for i in emails:
                cursor.execute('INSERT INTO emails (email) VALUES (%s)', (i,))
        engine.commit()
        cursor.close()
    except psycopg2.errors:
        pass

# =========================== Запись номеров телефонов в бд ===========================
async def write_phones(state):
    try:
        cursor = engine.cursor()
        async with state.proxy() as data:
            phones = data["phone"].split("\n")
            for i in phones:
                cursor.execute('INSERT INTO phones (phone_number) VALUES (%s)', (i,))
        engine.commit()
        cursor.close()
    except psycopg2.errors:
        pass

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(get_repl_logs, Text(equals='/get_repl_logs', ignore_case=True))
    dp.register_message_handler(get_emails, Text(equals='/get_emails', ignore_case=True))
    dp.register_message_handler(get_phone_numbers, Text(equals='/get_phone_numbers', ignore_case=True))
