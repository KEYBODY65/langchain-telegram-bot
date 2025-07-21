from aiogram import Bot, Dispatcher
import logging
import uvloop
from config.settings import Settings
from bot_utils.handlers import router


settings = Settings()

token = settings.BOT_TOKEN


async def start_bot(token: token):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - '  # логирование нужно для отображения результата работы хендлера: is handled / is not handled
                               '%(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s')

    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_router(router=router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    uvloop.run(start_bot(token=token))
