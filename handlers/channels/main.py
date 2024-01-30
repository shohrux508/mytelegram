from aiogram.types import CallbackQuery

from keyboards.inline.main_btns import AdminButton
from loader import dp, bot
from shortcuts.main_shortcuts import filter_data, get_channel_as_text
from utils.db_api.manage import Channel


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('set_required'))
async def requirement_h(call: CallbackQuery):
    data = filter_data(call.data, 'set_required')
    status, channel_id = data.split('+')
    try:
        Channel(call.from_user.id).set_required(status, channel_id)
        await call.answer('Успешно!')
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=get_channel_as_text(channel_id), reply_markup=await AdminButton().manage_channel(channel_id))

    except:
        await call.answer('Не получилось внести изменения!')

