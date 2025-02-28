from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from Env_generation.environment_generation import token

# регистрация токена
st = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=st)