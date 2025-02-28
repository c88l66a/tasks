from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from Env_generation.environment_generation import rm_host, rm_port, rm_user, rm_password
from Logging_module import log_module
from create_bot import bot

import paramiko

# Создание клиента
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Добавляем ключ хоста автоматически

#  ============================== О релизе ==============================
async def get_release(message: types.message):
    try:
        # Подключение к серверу
        client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
        # Выполнение команды
        stdin, stdout, stderr = client.exec_command("cat /etc/os-release")
        await message.answer(f"Результат выполнения команды:\n\n{stdout.read().decode()}")
    finally:
        # Закрытие соединения
        client.close()
    
    log_module.logger.info(f"CHAPTER : /get_release, TELEGRAM_ID : {message.from_user.id}")

#  ============= Об архитектуры процессора, имени хоста системы и версии ядра =============
async def get_uname(message: types.message):
    try:
        client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
        stdin, stdout, stderr = client.exec_command("uname -a")
        await message.answer(f"Результат выполнения команды:\n\n{stdout.read().decode()}")
    finally:
        client.close()

    log_module.logger.info(f"CHAPTER : /get_uname, TELEGRAM_ID : {message.from_user.id}")
    

#  ======================================= О времени работы =======================================
async def get_uptime(message: types.message):
    try:
        client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
        stdin, stdout, stderr = client.exec_command("uptime")
        await message.answer(f"Результат выполнения команды:\n\n{stdout.read().decode()}")
    finally:
        client.close()

    log_module.logger.info(f"CHAPTER : /get_uptime, TELEGRAM_ID : {message.from_user.id}")

# ======================== Сбор информации о состоянии файловой системы ========================
async def get_df(message: types.message):
    try:
        client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
        stdin, stdout, stderr = client.exec_command("df -h")
        await message.answer(f"Результат выполнения команды:\n\n{stdout.read().decode()}")
    finally:
        client.close()

    log_module.logger.info(f"CHAPTER : /get_df, TELEGRAM_ID : {message.from_user.id}")

# ======================== Сбор информации о состоянии оперативной памяти ========================
async def get_free(message: types.message):
    try:
        client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
        stdin, stdout, stderr = client.exec_command("free")
        await message.answer(f"Результат выполнения команды:\n\n{stdout.read().decode()}")
    finally:
        client.close()

    log_module.logger.info(f"CHAPTER : /get_free, TELEGRAM_ID : {message.from_user.id}")

# ========================== Сбор информации о производительности системы ==========================
async def get_mpstat(message: types.message):
    try:
        client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
        stdin, stdout, stderr = client.exec_command("mpstat -P ALL")
        await message.answer(f"Результат выполнения команды:\n\n{stdout.read().decode()}")
    finally:
        client.close()

    log_module.logger.info(f"CHAPTER : /get_mpstat, TELEGRAM_ID : {message.from_user.id}")

# =============== Сбор информации о работающих в данной системе пользователях ===============
async def get_w(message: types.message):
    try:
        client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
        stdin, stdout, stderr = client.exec_command("w")
        await message.answer(f"Результат выполнения команды:\n\n{stdout.read().decode()}")
    finally:
        client.close()

    log_module.logger.info(f"CHAPTER : /get_w, TELEGRAM_ID : {message.from_user.id}")
    
# =============================== Последние 10 входов в систему ===============================
async def get_auths(message: types.message):
    try:
        client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
        stdin, stdout, stderr = client.exec_command("last -n 10")
        await message.answer(f"Результат выполнения команды:\n\n{stdout.read().decode()}")
    finally:
        client.close()

    log_module.logger.info(f"CHAPTER : /get_auth, TELEGRAM_ID : {message.from_user.id}")
    

# ============================== Последние 5 критических события ==============================
async def get_critical(message: types.message):
    try:
        client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
        stdin, stdout, stderr = client.exec_command("journalctl -p crit -n 5")
        await message.answer(f"Результат выполнения команды:\n\n{stdout.read().decode()}")
    finally:
        client.close()

    log_module.logger.info(f"CHAPTER : /get_critical, TELEGRAM_ID : {message.from_user.id}")
    

# ========================== Сбор информации о запущенных процессах ==========================
async def get_ps(message: types.message):
    try:
        client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
        stdin, stdout, stderr = client.exec_command("ps -aux")
        with open("./tmp.txt", "wb") as file:
            file.write(stdout.read())
        await bot.send_document(chat_id=message.chat.id, document=open("./tmp.txt","rb"), caption=
                                f"Результат выполнения команды в виде отчета (так как размер сообщение слишком большой)")
    finally:
        client.close()
        

    log_module.logger.info(f"CHAPTER : /get_ps, TELEGRAM_ID : {message.from_user.id}")


# ========================== Сбор информации об используемых портах ===========================
async def get_ss(message: types.message):
    try:
        client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
        stdin, stdout, stderr = client.exec_command("ss -tua")
        await message.answer(f"Результат выполнения команды:\n\n{stdout.read().decode()}")
    finally:
        client.close()

    log_module.logger.info(f"CHAPTER : /get_ss, TELEGRAM_ID : {message.from_user.id}")

 
        
# ========================= Сбор информации об установленных пакетах =========================
class for_apt_list_all_or_single(StatesGroup):
    first_step = State()
    second_step = State()
    
async def get_apt_list(message: types.message):
    await message.answer("В каком формате предоставить информацию о deb-пакетах:\n/one_deb_packet\n/all_deb_packet")
    await for_apt_list_all_or_single.first_step.set()

    
async def all_deb_packet(message: types.message, state: FSMContext):
    if message.text == "/all_deb_packet":
        try:
            client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
            stdin, stdout, stderr = client.exec_command("dpkg-query -f '${'binary:Package'}\n' -W")
            with open("./tmp.txt", "wb") as file:
                file.write(stdout.read())
            await bot.send_document(chat_id=message.chat.id, document=open("./tmp.txt","rb"), caption=
                                    f"Результат выполнения команды в виде отчета (так как размер сообщение слишком большой)")
        finally:
            client.close()
        
        await state.finish()
        log_module.logger.info(f"CHAPTER : /get_apt_list, TELEGRAM_ID : {message.from_user.id}")
    
    elif message.text == "/one_deb_packet":
        await message.answer("Какой deb-пакет нужно найти ?")
        await for_apt_list_all_or_single.second_step.set()
        
    else:
        await message.answer("Ошибка ввода")
        await state.finish()
    

async def one_deb_packet(message: types.message, state: FSMContext):
    try:
        client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
        stdin, stdout, stderr = client.exec_command(f"apt list --installed | grep -i {message.text}")
        
        await message.answer(f"Результат выполнения команды:\n\n{stdout.read().decode()}")
        
    finally:
        client.close()
    
    await state.finish()
    log_module.logger.info(f"CHAPTER : /get_apt_list, TELEGRAM_ID : {message.from_user.id}")
    
# =========================== Сбор информации о запущенных сервисах ===========================
async def get_services(message: types.message):
    try:
        client.connect(hostname=rm_host, port=rm_port, username=rm_user, password=rm_password)
        
        session = client.get_transport().open_session()
        session.set_combine_stderr(True)
        session.get_pty()
        session.exec_command("sudo bash -c 'systemctl list-units --type=service --state=running --no-page'")
        
        stdin = session.makefile('wb', -1)
        stdout = session.makefile('rb', -1)
        
        stdin.write(rm_password + '\n')       
        await message.answer(f"Результат выполнения команды:\n\n{stdout.read().decode()}")
    finally:
        client.close()

    log_module.logger.info(f"CHAPTER : /get_services, TELEGRAM_ID : {message.from_user.id}")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(get_release, Text(equals='/get_release', ignore_case=True))
    dp.register_message_handler(get_uname, Text(equals='/get_uname', ignore_case=True))
    dp.register_message_handler(get_uptime, Text(equals='/get_uptime', ignore_case=True))
    dp.register_message_handler(get_df, Text(equals='/get_df', ignore_case=True))
    dp.register_message_handler(get_free, Text(equals='/get_free', ignore_case=True))
    dp.register_message_handler(get_mpstat, Text(equals='/get_mpstat', ignore_case=True))
    dp.register_message_handler(get_w, Text(equals='/get_w', ignore_case=True))
    dp.register_message_handler(get_auths, Text(equals='/get_auths', ignore_case=True))
    dp.register_message_handler(get_critical, Text(equals='/get_critical', ignore_case=True))
    dp.register_message_handler(get_ps, Text(equals='/get_ps', ignore_case=True))
    dp.register_message_handler(get_ss, Text(equals='/get_ss', ignore_case=True))
    dp.register_message_handler(get_apt_list, Text(equals='/get_apt_list', ignore_case=True))
    dp.register_message_handler(all_deb_packet, state=for_apt_list_all_or_single.first_step)
    dp.register_message_handler(one_deb_packet, state=for_apt_list_all_or_single.second_step)
    dp.register_message_handler(get_services, Text(equals='/get_services', ignore_case=True))
    
    
    
    
