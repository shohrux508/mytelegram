from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.inline.main_btns import AdminButton
from keyboards.inline.office_keyboards import myCabinetBtn
from loader import dp, bot
from shortcuts.main_shortcuts import filter_data, get_users_as_text, manage_user_kb
from states.StatesGroup import Chat
from utils.db_api.manage import search_user, ManageUser




@dp.message_handler(Text(contains='Пользователи'))
async def users(msg: Message):
    message = get_users_as_text(sort_by=False, filter_by=False, page=1, paginate_by=5)
    await msg.answer(message,
                     reply_markup=AdminButton().manage_users_list(sort_by=False, filter_by=False, page=1,
                                                                  paginate_by=5))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("prev-page"))
async def answer(call: CallbackQuery):
    datas = (filter_data(call.data, function='prev-page')).split("+")
    sort_by = datas[0]
    filter_by = datas[1]
    paginate_by = int(datas[3])
    page = int(datas[2])
    if page > 1:
        page = page - 1
    else:
        await call.answer('Первая страница!')

    text = get_users_as_text(sort_by, filter_by, page, paginate_by)
    try:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=AdminButton().manage_users_list(sort_by, filter_by, page, paginate_by))
    except:
        await call.answer('Ошибка!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("next-page"))
async def answer(call: CallbackQuery):
    datas = (filter_data(call.data, function='next-page')).split("+")
    sort_by = datas[0]
    filter_by = datas[1]
    paginate_by = int(datas[3])
    page = int(datas[2]) + 1
    try:
        text = get_users_as_text(sort_by, filter_by, page, paginate_by)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=AdminButton().manage_users_list(sort_by, filter_by, page, paginate_by))

    except:
        await call.answer('Последняя страница!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('refresh'))
async def answer(call: CallbackQuery):
    datas = (filter_data(call.data, function='refresh')).split("+")
    sort_by = datas[0]
    filter_by = datas[1]
    paginate_by = int(datas[2])
    page = int(datas[3])
    text = get_users_as_text(sort_by, filter_by, paginate_by, page)
    try:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=AdminButton().manage_users_list(sort_by, filter_by, page, paginate_by))
    except:
        await call.answer('Ошибка!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('filter-by-'))
async def filter_by(call: CallbackQuery):
    data = filter_data(call.data, 'filter-by-')
    text = get_users_as_text(sort_by=False, filter_by=data, page=1, paginate_by=5)
    try:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=AdminButton().manage_users_list(sort_by=False, filter_by=data, page=1,
                                                                                 paginate_by=5))
    except:
        await call.answer('Ошибка!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('search-user'))
async def search_user_h1(call: CallbackQuery, state: FSMContext):
    message = await bot.send_message(chat_id=call.from_user.id, text='Введите номер телефона или Telegram ID: \n'
                                                                     'Отменить: /break')
    await state.update_data(message_id=message.message_id)
    await state.set_state(Chat.get_id_to_search.state)


@dp.message_handler(state=Chat.get_id_to_search.state)
async def search_user_h(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if 'break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
        return False
    if search_user(msg.text) == False:
        await msg.answer('Пользователь не найден!')
    else:
        user_id, text = search_user(msg.text)
        await msg.answer(text, reply_markup=manage_user_kb(user_id, msg.from_user.id))
    await state.finish()
