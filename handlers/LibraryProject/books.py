import requests
from aiogram import types
from keyboards.inline.main_btns import manage_books
from loader import dp, bot
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from shortcuts.main_shortcuts import get_books_as_text, get_book


@dp.message_handler(Text(contains='Все книги'))
async def books_list(msg: Message):
    response = requests.get(url='https://plcengineer.pythonanywhere.com/app1/api/v1/books/').json()
    text, count = get_books_as_text(msg.from_user.id, 1)
    await msg.answer(text, reply_markup=manage_books(current_page=1, response=response, count=count))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('get_book'))
async def get_book_h(call: CallbackQuery):
    data = call.data.split(',')
    index = (data[0]).replace('get_book=', '')
    page = (data[1]).replace('pag=', '')
    book = get_book(page, index)
    if book[0] == False:
        await call.answer(book[1])
    else:
        status, text, file_path = get_book(page, index)

        input_file = types.InputFile(file_path)
        await bot.send_document(chat_id=call.from_user.id, document=input_file, caption=text)


@dp.message_handler(Text(contains='Состояние сервера'))
async def server(msg: Message):
    username = 'plcengineer'
    token = '5a2962ff1e494da9095e8af7ca9b45f7bc11ab23'
    response = requests.get(
        f'https://www.pythonanywhere.com/api/v0/user/{username}/cpu/'.format(
            username=username
        ),
        headers={'Authorization': f'Token {token}'.format(token=token)}
    )
    if response.status_code == 200:
        print('CPU quota info:')
        print(response.content)
    else:
        print('Got unexpected status code {}: {!r}'.format(response.status_code, response.content))