from loader import dp, bot
from aiogram.types import CallbackQuery, Message

from shortcuts.main_shortcuts import filter_data


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('remove-btn'))
async def remove_btn(call: CallbackQuery):
    msg_id = filter_data(call.data, 'remove-btn')
    if msg_id:
        await bot.delete_message(chat_id=call.from_user.id, message_id=msg_id)
    await call.answer('❌')
    await call.message.delete()
