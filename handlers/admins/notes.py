from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message

from handlers.admins.office_tools import myNotes
from keyboards.inline.office_keyboards import myCabinetBtn, myNotesBtn
from keyboards.one_time_keyboards import button
from loader import dp, bot
from shortcuts.main_shortcuts import filter_data
from states.StatesGroup import NoteSession
from utils.db_api.manage import ManageUser


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('admin/notes'))
async def notes(call: CallbackQuery):
    if myNotesBtn()[0] == False:
        notes = 'Добавьте заметку'
    else:
        notes = 'Мои заметки'
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f"{notes}",
                                reply_markup=myNotesBtn()[1])


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('notes/page/'))
async def switch_page(call: CallbackQuery):
    page, function = (filter_data(call.data, 'notes/page/')).split(',')
    page = int(page)
    try:
        myNotesBtn(page)
    except:
        await call.answer('Заметки отсутствуют!')
        return

    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f'{notes}\n'
                                                                                                    f'{page}-стр',
                                reply_markup=myNotesBtn(page=page, function=function)[1])


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('see-note/'))
async def get_Note(call: CallbackQuery):
    note_id, page = (filter_data(call.data, 'see-note/')).split(',')
    note = (myNotes().get(pk=note_id))[2]
    await call.answer(f'{note_id}.Заметка: {note["title"]}\n'
                      f'{note["text"]}\n'
                      f'Дата добавления: {note["date_added"]}', show_alert=True)


@dp.callback_query_handler(text='notes/delete')
async def delete_mode(call: CallbackQuery):
    await bot.send_message(chat_id=call.from_user.id, text='Выберите для удаления!',
                           reply_markup=myNotesBtn(function='delete'))


@dp.callback_query_handler(text='notes/new')
async def create_note(call: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=call.from_user.id, text='Название заметки\n'
                                                           'Отменить: /break')
    await state.update_data(msg_id=call.message.message_id)
    await state.set_state(NoteSession.get_title.state)


@dp.message_handler(state=NoteSession.get_title.state)
async def get_title(msg: Message, state: FSMContext):
    msg_id = (await state.get_data()).get("msg_id")
    if '/break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg_id)
        return
    await state.update_data(title=msg.text)
    await state.set_state(NoteSession.get_text.state)
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    await bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg_id, text='Напишите текст заметки\n'
                                                                                  'Отменить: /break')


@dp.message_handler(state=NoteSession.get_text.state)
async def get_text_h(msg: Message, state: FSMContext):
    msg_id = (await state.get_data()).get("msg_id")
    if '/break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg_id)
        return
    title = (await state.get_data()).get('title')
    text = msg.text
    response, status_code = myNotes().create(title, text)
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    if status_code == 201:
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg_id, text='Заметка создана',
                                    reply_markup=button('Проверить', f'{response["id"]}, {None}', 'see-note/'))
    else:
        await bot.send_message(chat_id=msg.from_user.id, text=response)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete-note/'))
async def delete_Note(call: CallbackQuery):
    note_id, page = (filter_data(call.data, 'delete-note/')).split(',')
    page = int(page)
    response = myNotes().delete(pk=note_id)
    await call.answer(f'{response}')
    if myNotesBtn(page)[0] == False:
        text = 'Заметки были удалены!'
    else:
        text = 'Мои заметки'
    await bot.edit_message_text(chat_id=call.from_user.id, text=text, message_id=call.message.message_id,
                                reply_markup=myNotesBtn(function='delete', page=page)[1])
