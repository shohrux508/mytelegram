from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from keyboards.inline.office_keyboards import myCabinetBtn
from loader import dp
from utils.db_api.manage import ManageUser


@dp.message_handler(Text(contains='Мой кабинет'))
async def answer(msg: Message):
    if not ManageUser(msg.from_user.id).is_admin():
        return
    await msg.answer('Ваш личный кабинет', reply_markup=myCabinetBtn(message_id=msg.message_id))
