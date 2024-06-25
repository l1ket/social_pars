import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers_bot import common
from start_pars import start, select_all_user


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(token='')

    dp.include_router(common.router)

    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(pr, "cron", day_of_week='mon', hour=9, minute=1)

    logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)

    await bot.delete_webhook(
        drop_pending_updates=True
        )  # Скипает все новые сообщения
    await dp.start_polling(bot)

async def pr():
    print('start')
    bot = Bot(token='')
    inst, yt, tt = await start()
    res = select_all_user()
    for i in res:
        await bot.send_message(chat_id=i[0], text=f'inst:\n{inst}\n\nyt:\n{yt}\n\ntt:\n{tt}')


if __name__ == '__main__':
    asyncio.run(main())
