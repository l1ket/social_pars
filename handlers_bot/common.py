from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from start_pars import add_user, table_users_create, select_user

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    us_id = message.from_user.id
    table_users_create()
    res = select_user(us_id)
    if res == []:
        add_user(us_id=us_id)
    elif res[0][0] != us_id:
        add_user(us_id=us_id)
        
    await message.answer(
        text="Вы добавлены в рассылку."
    )


@router.message(Command('stats'))
async def cmd_main(message: Message):
   await message.answer(text='123')