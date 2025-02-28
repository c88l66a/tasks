from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import re

from Logging_module import log_module
from Functionals import interaction_with_db

EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')
PHONE_PATTERN = re.compile(r'(?:\+7|8)[-\s]?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}')

class find_phone_or_mail(StatesGroup):
    text_with_emails = State()
    text_with_phones = State()
    write_emails = State()
    write_phones = State()

async def input_text_with_emails(message: types.message):
    await message.answer("Введите текст для поиска Email-адресов:")
    await find_phone_or_mail.text_with_emails.set()

async def output_found_emails(message: types.message, state: FSMContext):

    # Ищем все email-адреса в тексте
    emails = EMAIL_PATTERN.findall(message.text)
    if emails:
        # Если найдены email-адреса, отправляем их пользователю
        email_list = '\n'.join(emails)
        await message.answer(f"Найденные email-адреса:\n{email_list}\n\n Хотите сохранить их в БД ?\n/yes\n/no")
        # список найденных Email-адресов, для записи в БД, state сохраняет все взаиомдействие в процессе состояния сообщений между ботом и пользователем
        async with state.proxy() as data:
            data['email'] = email_list
        await find_phone_or_mail.write_emails.set()
    else:
        # Если email-адреса не найдены
        await message.answer("В тексте не найдено ни одного email-адреса.")
        await state.finish()
    log_module.logger.info(f"CHAPTER : /find_email, TELEGRAM_ID : {message.from_user.id}")

async def write_found_emails_in_db(message: types.message, state: FSMContext):
    if message.text == "/no":
        await message.answer("OK")
        await state.finish()
    elif message.text == "/yes":
        await interaction_with_db.write_emails(state)
        await message.answer("Email-адреса были записаны в БД")
        await state.finish()



async def input_text_with_phones(message: types.message):
    await message.answer("Введите текст для поиска номеров телефона:")
    await find_phone_or_mail.text_with_phones.set()

async def output_found_phones(message: types.message, state: FSMContext):
    # Ищем все номера в тексте
    phones = PHONE_PATTERN.findall(message.text)
    if phones:
        # Если найдены номера, отправляем их пользователю
        phone_list = '\n'.join(phones)
        
        await message.answer(f"Найденные номера:\n{phone_list}\n\n Хотите сохранить их в БД ?\n/yes\n/no")
        # список найденных телефонов, для записи в БД, state сохраняет все взаиомдействие в процессе состояния сообщений между ботом и пользователем
        async with state.proxy() as data:
            data['phone'] = phone_list
            
        await find_phone_or_mail.write_phones.set()
    else:
        # Если номера не найдены
        await message.answer("В тексте не найдено ни одного номера")
        await state.finish()
    
    log_module.logger.info(f"CHAPTER : /find_phone_number, TELEGRAM_ID : {message.from_user.id}")

async def write_found_phones_in_db(message: types.message, state: FSMContext):
    if message.text == "/no":
        await message.answer("OK")
        await state.finish()
        
    elif message.text == "/yes":
        await interaction_with_db.write_phones(state)
        await message.answer("номера телефонов были записаны в БД")
        await state.finish()







def register_handlers(dp: Dispatcher):
    
    dp.register_message_handler(input_text_with_emails, Text(equals='/find_email', ignore_case=True))
    dp.register_message_handler(output_found_emails, state=find_phone_or_mail.text_with_emails)
    dp.register_message_handler(write_found_emails_in_db, state=find_phone_or_mail.write_emails)
    
    dp.register_message_handler(input_text_with_phones, Text(equals='/find_phone_number', ignore_case=True))
    dp.register_message_handler(output_found_phones, state=find_phone_or_mail.text_with_phones)
    dp.register_message_handler(write_found_phones_in_db, state=find_phone_or_mail.write_phones)
