from aiogram.utils import executor
from create_bot import dp

from Functionals import search_in_text
from Functionals import password_check
from Functionals import monitoring
from Functionals import interaction_with_db

# запуск обработчиков, в которых находится функционал бота
search_in_text.register_handlers(dp)
password_check.register_handlers(dp)
monitoring.register_handlers(dp)
interaction_with_db.register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)