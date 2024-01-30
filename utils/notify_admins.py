import logging

from aiogram import Dispatcher

from data.config import ADMINS
from keyboards.one_time_keyboards import button


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен", reply_markup=button('❌', '', 'remove-btn'))

        except Exception as err:
            logging.exception(err)
