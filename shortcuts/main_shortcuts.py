import os
from loader import bot
import requests
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from openpyxl import Workbook
from data.database import *
from datetime import datetime
import requests as r
from keyboards.one_time_keyboards import button
from utils.db_api.manage import ManageUser


def filter_data(data, function, split_key=None):
    context = data.replace(function, '')
    if split_key:
        context = context.split(split_key)
    return context


async def send_message_to_admin(msg):
    list = ManageUser('').list(select_id=True, filter_by='admin', period=False)
    try:
        for id in list:
            await bot.send_message(chat_id=id, text=msg.text,
                                   reply_markup=button('Ответить', f'{msg.from_user.id}+{msg.message_id}', 'answer'))
    except:
        return False
    return True


def get_users_as_text(sort_by, filter_by, page, paginate_by):
    if filter_by == 'admins':
        title = 'администраторов'
        cur.execute(f'''SELECT * FROM users WHERE is_admin > 0''')
    elif filter_by == 'blocked-users':
        title = 'заблокированных пользователей'
        cur.execute(f'''SELECT * FROM users WHERE is_blocked > 0''')
    else:
        title = 'всех пользователей'
        cur.execute(f'''SELECT * FROM users''')
    users = cur.fetchall()
    if sort_by != False:
        if sort_by == 'name':
            users.sort(key=lambda users: users[1])
        elif sort_by == 'datetime':
            users.sort(key=lambda user: user[5])
        elif sort_by == 'id':
            users.sort(key=lambda user: user[6])
        else:
            pass
    count = 1
    full_text = []
    full_text.append(f'Список {title}: '
                     f'{datetime.now().strftime("%H:%M:%S")}\n')
    for user in users:
        text = (f'{count}.{user[3]}\n'
                f'Порядковый номер: {user[6]}\n'
                f'Телеграм id: {user[0]}\n'
                f'Номер телефонa: {user[4]}\n'
                f'Дата Присоединения: {user[5]}\n'
                f'\n'
                f'------------------------------')
        full_text.append(text)
        count += 1
    chunked_lists = [full_text[i:i + paginate_by] for i in range(0, len(full_text), paginate_by)]
    chunked_lists[page - 1].append(f'Всего пользователей: {count - 1}\n\n'
                                   f'Страница: {page} из {len(chunked_lists)}')

    # chunked_lists[page-1].append(f'Общее количество {title}: {count - 1}\n')
    message = '\n'.join(full_text)
    message2 = '\n'.join(chunked_lists[page - 1])

    return message2


def manage_user_kb(user_id, msg_from_user_id):
    phone = (ManageUser(user_id).get(by=False, table_name="", data=""))[4]
    if "+" not in phone:
        phone = (f"+{phone}")
    ban = InlineKeyboardButton(text='Забанить ⛔️', callback_data=f"ban1+{user_id}")
    unban = InlineKeyboardButton(text='Разбанить ✅', callback_data=f"ban0+{user_id}")
    admin = InlineKeyboardButton(text='Администратор ✅️', callback_data=f"admin1+{user_id}")
    disadmin = InlineKeyboardButton(text='Удалить из админов ⛔️', callback_data=f"admin0+{user_id}")
    send_message_btn = InlineKeyboardButton(text='Написать 📝', callback_data=f'send_message_to_user{user_id}')
    find_profile_btn = InlineKeyboardButton(text='Найти профиль 🔍',
                                            url=f'https://t.me/{phone}')
    info_kb = InlineKeyboardMarkup().add(send_message_btn, find_profile_btn)
    if ManageUser(user_id).is_admin():
        info_kb.add(disadmin)
    else:
        info_kb.add(admin)

    if ManageUser(user_id).is_blocked():
        info_kb.add(unban)
    else:
        info_kb.add(ban)

    if user_id != msg_from_user_id:
        return info_kb
    else:
        return button('❌', '', 'delete_message')


def download_users_excel_file():
    wb = Workbook()
    ws = wb.active
    users = ManageUser(user_id='').list(select_id=False, filter_by=False, period=False)
    for user in users:
        ws.append(user)

    wb.save(f'data/excel/Users{len(users)}.xlsx')
    return len(users)


def get_channel_as_text(channel_id):
    cur.execute(f'''SELECT * FROM channels WHERE channel_id = {channel_id}''')
    channel = cur.fetchone()
    text = (f'{channel[2]}.\n'
            f'Идентификационный номер: {channel[0]}')

    return text


def get_authors_as_text(user_id, page):
    if page:
        response = r.request(method='GET',
                             url=f'https://plcengineer.pythonanywhere.com/app1/api/v1/authors/?page={page}')
    else:
        response = r.request(method='GET', url=f'https://plcengineer.pythonanywhere.com/app1/api/v1/authors/')
    if response.status_code == 200:
        authors = response.json()['results']
        full_text = []
        full_text.append(f'Список всех авторов: {datetime.now().strftime("%H:%M:%S")}\n')
        count = 1
        for i in authors:
            text = (f'Автор: {i["id"]}\n'
                    f'Имя: {i["name"]}\n'
                    f'Био: {i["bio"]}\n'
                    f'Пол: {i["gender"]}\n'
                    f'Возраст: {i["age"]}\n---------')
            full_text.append(text)
            count += 1
        full_text.append(f'Всего авторов: {response.json()["count"]}\n'
                         f'Страница: {response.json()["count"]}')
        overall_text = '\n'.join(full_text)
        return overall_text, count
    return False


def get_books_as_text(user_id, page):
    if page:
        response = r.request(method='GET', url=f'https://plcengineer.pythonanywhere.com/app1/api/v1/books/?page={page}')
    else:
        response = r.request(method='GET', url=f'https://plcengineer.pythonanywhere.com/app1/api/v1/books')
    if response.status_code == 200:
        authors = response.json()['results']
        full_text = []
        full_text.append(f'Список всех книг: {datetime.now().strftime("%H:%M:%S")}\n')
        count = 1
        for i in authors:
            text = (f'{count}.Книга N:{i["id"]}: {i["title"]}\n'
                    f'Автор: {i["author"]}\n'
                    f'Дата создания: {i["date"]}\n---------')
            count += 1
            full_text.append(text)
        full_text.append(f'Всего книг: {response.json()["count"]}\n'
                         f'Страница: {response.json()["count"]}')
        overall_text = '\n'.join(full_text)
        return overall_text, count
    return response.json()


def download_file(file_name):
    file_path = f'media/books/{file_name}'
    if os.path.exists(file_path):
        return True, file_path
    response = requests.get(url=f'https://plcengineer.pythonanywhere.com/media/books/{file_name}')
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return True, file_path
    else:
        return False, response.json()


def get_book(page, index):
    response = requests.get(url=f'https://plcengineer.pythonanywhere.com/app1/api/v1/books/?page={page}')
    try:
        list = (response.json())['results']
    except:
        return response
    book = list[int(index) - 1]
    text = (f'Книга N:{book["id"]}: {book["title"]}\n'
            f'Автор: {book["author"]}\n\n'
            f'Дата создания: {book["date"]}\n---------')
    file = book['file']
    file_name = (file.split('/'))[5]
    data = download_file(file_name)
    if data[0] == True:
        file_path = data[1]
        return True, text, file_path
    else:
        return False, data[1]
