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


# ============= Регулярка для номера телефона =============
# 1. (?:\+7|8)
# (?: ... ): Группа без сохранения (не захватывает совпадение для дальнейшего использования в результате).
# \+7: Совпадает с символом + (экранирован с помощью \) и цифрой 7. Это формат телефонного кода для России.
# |: Логическое "ИЛИ".
# 8: Совпадает с цифрой 8.
# В итоге: Совпадает либо с +7, либо с 8 в начале номера.
# 2. [-\s]?
# [-\s]: Совпадает с одним из символов:
# - (дефис).
# \s (любой пробельный символ: пробел, табуляция, перевод строки).
# ?: Указывает, что символ из набора может присутствовать, а может отсутствовать (0 или 1 раз).
# В итоге: После +7 или 8 может быть опциональный дефис или пробел.
# 3. \(?\d{3}\)?
# \(?: Опциональная открывающая скобка ( (может быть, а может не быть).
# \d{3}: Совпадает ровно с 3 цифрами.
# \)?: Опциональная закрывающая скобка ) (может быть, а может не быть).
# В итоге: Совпадает с кодом региона (3 цифры), который может быть обёрнут в круглые скобки или записан без них (например, 123 или (123)).
# 4. [-\s]?
# Это такой же опциональный разделитель, как в шаге 2, для разделения между кодом региона и следующей частью номера.
# 5. \d{3}
# Совпадает ровно с 3 цифрами — первая часть основного номера телефона.
# 6. [-\s]?
# Ещё один опциональный разделитель между первой и второй частями номера.
# 7. \d{2}
# Совпадает ровно с 2 цифрами — первая половина второй части номера.
# 8. [-\s]?
# Опциональный разделитель между двумя частями второй половины номера.
# 9. \d{2}
# Совпадает ровно с 2 цифрами — вторая половина второй части номера.


# ============= Регулярка для email =============
# . \b
# Это граница слова, которая указывает, что совпадение должно начинаться и заканчиваться на границе слова.
# Это помогает исключить "лишние" символы вокруг email-адреса, например, если он находится в тексте без пробелов.
# 2. [A-Za-z0-9._%+-]+
# Совпадает с одним или несколькими символами (благодаря +), которые могут быть:
# A-Za-z: Любая заглавная или строчная латинская буква.
# 0-9: Любая цифра.
# ._%+-: Специальные символы ., _, %, +, -.
# Это соответствует локальной части email-адреса (т.е. части до символа @).
# 3. @
# Совпадает с символом "@".
# Это обязательный разделитель между локальной частью и доменной частью email-адреса.
# 4. [A-Za-z0-9.-]+
# Совпадает с одним или несколькими символами, которые могут быть:
# A-Za-z: Любая заглавная или строчная латинская буква.
# 0-9: Любая цифра.
# .-: Символы . и - (точка и дефис).
# Это соответствует доменному имени (часть email после @), включая поддомены (например, sub.example).
# 5. \.[A-Za-z]{2,}
# \.: Совпадает с символом точки ..
# [A-Za-z]{2,}: Совпадает с последовательностью из двух или более букв (латинских заглавных или строчных).
# Это соответствует доменному суффиксу (например, .com, .org, .net).
# 6. \b
# Закрывающая граница слова для завершения совпадения.