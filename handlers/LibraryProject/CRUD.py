import requests
import requests as r
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.inline.main_btns import gender_btns, submit_btns, manage_authors, detail_btns, manage_books
from loader import dp, bot
from shortcuts.main_shortcuts import filter_data, get_authors_as_text, get_books_as_text
from states.StatesGroup import AuthorCreateState
from utils.db_api.manage import ManageUser


@dp.message_handler(Text(contains='Все авторы'))
async def all_authors(msg: Message):
    await msg.answer(get_authors_as_text(msg.from_user.id, page=False), reply_markup=manage_authors(current_page=1))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('admin/authors/page'))
async def switch_page(call: CallbackQuery):
    page = filter_data(call.data, 'admin/authors/page')
    data = get_authors_as_text(call.from_user.id, page)
    text = data[0]
    keyboard = manage_authors(current_page=page)
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                reply_markup=keyboard)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('admin/books/page'))
async def switch_page(call: CallbackQuery):
    page = filter_data(call.data, 'admin/books/page=')
    response = requests.get(url=f'https://plcengineer.pythonanywhere.com/app1/api/v1/books/?page={page}').json()
    data = get_books_as_text(user_id=call.from_user.id, page=page)
    text = data[0]
    keyboard = manage_books(current_page=page, response=response, count=data[1])
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                reply_markup=keyboard)

@dp.message_handler(Text(contains='Новый автор'))
async def create_author(msg: Message, state: FSMContext):
    message = await msg.answer('Как зовут нового автора?\n'
                               'Отменить: /break')
    await state.update_data(message_id=message.message_id)
    await state.set_state(AuthorCreateState.get_name.state)


@dp.message_handler(state=AuthorCreateState.get_name.state)
async def get_name(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if 'break' in msg.text:
        await state.finish()
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Отменено!')
        return
    await state.update_data(name=msg.text)
    await state.set_state(AuthorCreateState.get_age.state)
    await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Введите возраст автора!\n'
                                                                                      'Отменить: /break')


@dp.message_handler(state=AuthorCreateState.get_age.state)
async def get_age(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if 'break' in msg.text:
        await state.finish()
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Отменено!')
        return
    await state.update_data(age=msg.text)
    await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Био автора: \n'
                                                                                      'Отменить: /break')
    await state.set_state(AuthorCreateState.get_bio.state)


@dp.message_handler(state=AuthorCreateState.get_bio.state)
async def get_bio(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if 'break' in msg.text:
        await state.finish()
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Отменено!')
        return
    await state.update_data(bio=msg.text)
    await state.set_state(AuthorCreateState.get_gender.state)
    await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Выберите: ',
                                reply_markup=gender_btns())


@dp.callback_query_handler(state=AuthorCreateState.get_gender.state)
async def get_gender(call: CallbackQuery, state: FSMContext):
    if 'break' in call.data:
        await state.finish()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Отменено!')
        return
    await state.update_data(gender=call.data)
    await state.set_state(AuthorCreateState.finish.state)
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Данные получены!',
                                reply_markup=submit_btns())


@dp.callback_query_handler(state=AuthorCreateState.finish.state)
async def finish_state(call: CallbackQuery, state: FSMContext):
    if 'break' in call.data:
        await state.finish()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Отменено!')
        return
    data = await state.get_data()
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    bio = data.get('bio')
    post = {'name': name, 'age': age, 'gender': gender, 'bio': bio}
    auth_token = (ManageUser(call.from_user.id).auth_token())[0]
    response = r.post(url='https://plcengineer.pythonanywhere.com/app1/api/v1/authors/new/', data=post,
                      headers={'Authorization': f'Token {auth_token}'})
    if response.status_code == 201:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text='Успешно сохранено!')
        id = response.json()['id']
        await bot.send_message(chat_id=call.from_user.id,
                               text=f"https://plcengineer.pythonanywhere.com/app1/api/v1/authors/{id}",
                               reply_markup=detail_btns(id))
    else:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=response.json())
    await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('detail'))
async def detail_view(call: CallbackQuery):
    id = filter_data(call.data, 'detail')
    auth_token = (ManageUser(call.from_user.id).auth_token())[0]
    response = r.get(url=f'https://plcengineer.pythonanywhere.com/app1/api/v1/authors/{id}',
                     headers={'Authorization': f'Token {auth_token}'})
    if response.status_code != 200:
        await call.answer(response.json())
        return
    author = response.json()
    await call.answer(f'Имя: {author["name"]}\n'
                      f'Био: {author["bio"]}\n'
                      f'Пол: {author["gender"]}\n'
                      f'Возраст: {author["age"]}\n', show_alert=True)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete'))
async def delete_view(call: CallbackQuery):
    id = filter_data(call.data, 'delete')
    auth_token = (ManageUser(call.from_user.id).auth_token())[0]
    response = r.delete(headers={"Authorization": f'Token {auth_token}'},
                        url=f'https://plcengineer.pythonanywhere.com/app1/api/v1/authors/{id}')
    if response.status_code == 204:
        await call.message.delete()
        await call.answer('Удалено из базы!')
    else:
        await call.answer('Не удалось удалить!\n'
                          f'{response.json()}', show_alert=True)











