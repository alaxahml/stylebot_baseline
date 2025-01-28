
import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers.user_handlers import user_router
# Настраиваем базовую конфигурацию логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main() -> None:

    # Загружаем конфиг в переменную config
    config: Config = load_config()


    photo_num = {"photo_num" : 0}


    # Инициализируем бот и диспетчер
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(photo_num=photo_num)

    # Регистрируем роутеры в диспетчере
    dp.include_router(user_router)


    #dp.update.outer_middleware(FirstOuterMiddleware())


    # Запускаем polling
    await dp.start_polling(bot)


asyncio.run(main())