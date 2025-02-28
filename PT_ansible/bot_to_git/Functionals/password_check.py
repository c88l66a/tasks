from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import re

from Logging_module import log_module

PASSWORD_PATTERN = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,}$")

class check_pass(StatesGroup):
    text_with_password = State()
    
async def input_password(message: types.message):
    await message.answer("Введите пароль для проверки")
    await check_pass.text_with_password.set()
    
async def password_check(message: types.message, state: FSMContext):
    # password = PASSWORD_PATTERN.findall(message.text)
    # if PASSWORD_PATTERN.match(message.text)
    
    if PASSWORD_PATTERN.match(message.text):
        await message.answer(f"Пароль сложный")
        await state.finish()
    else:
        await message.answer(f"Пароль простой")
        await state.finish()
        
    log_module.logger.info(f"CHAPTER : /verify_password, TELEGRAM_ID : {message.from_user.id}")
    
    
def register_handlers(dp: Dispatcher):
    
    dp.register_message_handler(input_password, Text(equals='/verify_password', ignore_case=True))
    dp.register_message_handler(password_check, state=check_pass.text_with_password)

# Объяснение регулярного выражения:
# ^ и $:

# Указывают на начало и конец строки, чтобы проверить пароль целиком.
# (?=.*[A-Z]):

# Указывает, что строка должна содержать хотя бы одну заглавную букву.
# (?=.*[a-z]):

# Указывает, что строка должна содержать хотя бы одну строчную букву.
# (?=.*\d):

# Указывает, что строка должна содержать хотя бы одну цифру.
# (?=.*[!@#$%^&*()]):

# Указывает, что строка должна содержать хотя бы один специальный символ из списка !@#$%^&*().
# [A-Za-z\d!@#$%^&*()]{8,}:

# Указывает, что пароль должен состоять из букв (заглавных и строчных), цифр и разрешённых специальных символов и иметь длину не менее 8 символов.

# passwords = [
#     "12345678",
#     "qwertyui",
#     "QWERTYUI",
#     "!!!!!!!!",
#     "1!!!!!!!",
#     "a!!!!!!!",
#     "A!!!!!!!",
#     "a2345678",
#     "A2345678",
#     "a!345678",
#     "A!345678",
#     "A!a45678",
# ]
