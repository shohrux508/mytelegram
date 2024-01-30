from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from keyboards.one_time_keyboards import button
from loader import dp, bot
from shortcuts.main_shortcuts import filter_data
from states.StatesGroup import Chat
from utils.db_api.manage import ManageUser


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('answer'))
async def answer(call: CallbackQuery, state: FSMContext):
    data = filter_data(call.data, 'answer')
    user_id, _message_id = data.split('+')
    message_id = await bot.send_message(chat_id=call.from_user.id, text='Напишите текст сообщения: ')
    await state.update_data(user_id=user_id, _message_id=_message_id, message_id=message_id)
    await state.set_state(Chat.get_message_to_answer.state)


@dp.message_handler(state=Chat.get_message_to_answer.state)
async def answer(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if 'break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
        return
    data = await state.get_data()
    user_id = data.get('user_id')
    _message_id = data.get('_message_id')
    await bot.send_message(chat_id=user_id, text=msg.text, reply_to_message_id=_message_id)
    await msg.answer('Успешно')
    await state.finish()


# edit
# 1
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('edit-msg-private'))
async def edit_msg_text(call: CallbackQuery, state: FSMContext):
    data = filter_data(call.data, 'edit_msg')
    user_id, _message_id = data.split('+')
    message_id = await bot.send_message(chat_id=call.from_user.id, text='Напишите новый текст сообщения!')
    await state.update_data(user_id=user_id, _message_id=_message_id, message_id=message_id)
    await state.set_state(Chat.edit_private_msg.state)


# 2
@dp.message_handler(state=Chat.edit_private_msg.state)
async def edit_private_msg(msg: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    message_id = data.get('message_id')
    _message_id = data.get('_message_id')
    try:
        await bot.edit_message_text(chat_id=user_id, message_id=_message_id, text=msg.text,
                                    reply_markup=button('Ответить', f'{user_id}+{msg.message_id}', 'answer'))
    except:
        await msg.answer('Не удалось изменить сообщение!\n'
                         'Возможно сообщение было удалено')

    await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id,
                                text=f'Успешно Изменено на: {msg.text}')
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)


# delete message from private user
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete-msg-private'))
async def delete_private_msg(call: CallbackQuery):
    data = filter_data(call.data, 'delete-msg-private')
    user_id, message_id = data.split('+')
    await bot.delete_message(chat_id=user_id, message_id=message_id)
    await call.answer(f'Удалено у пользователя -> {user_id}', show_alert=True)


# delete messages from all users
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete-sent-msgs'))
async def delete_sent_msgs(call: CallbackQuery):
    data = filter_data(call.data, 'delete-sent-msgs')
    message_id, users_count = data.split('+')
    list = ManageUser(call.from_user.id).list(select_id=True, filter_by='', period=[0, users_count])
    try:
        for id in list:
            await bot.delete_message(chat_id=id, message_id=message_id)
            message_id = int(message_id) + 1
            await call.answer('Удалено!')
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text='Удалено...')
    except:
        await call.answer('Не удалось удалить сообщения!', show_alert=True)


