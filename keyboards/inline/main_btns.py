from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.entertainment.tools import game_codes, generate_join_link
from loader import bot
from utils.db_api.check import is_required

btn = InlineKeyboardButton(text='❌', callback_data='remove-btn')


class AdminButton():

    def manage_sent_messages(self, message_id, count):
        btn1 = InlineKeyboardButton(text='Изменить сообщение', callback_data=f'edit-sent-msgs{message_id}+{count}')
        btn2 = InlineKeyboardButton(text='Удалить сообщение', callback_data=f'delete-sent-msgs{message_id}+{count}')
        keyboard = InlineKeyboardMarkup().add(btn1).add(btn2)
        return keyboard

    def manage_users_list(self, sort_by, filter_by, page, paginate_by):
        str = f'{sort_by}+{filter_by}+{page}+{paginate_by}'
        btn1 = InlineKeyboardButton(text='⬅️', callback_data=f'prev-page{str}')
        btn2 = InlineKeyboardButton(text='➡️', callback_data=f'next-page{str}')
        btn3 = InlineKeyboardButton(text='Все пользователи', callback_data=f'filter-by-users')
        btn4 = InlineKeyboardButton(text='Администраторы👨‍🚀', callback_data=f'filter-by-admins')
        btn5 = InlineKeyboardButton(text='Чёрный список', callback_data=f'filter-by-blocked-users')
        btn6 = InlineKeyboardButton(text='Искать 🔍', callback_data=f'search-user')
        btn7 = InlineKeyboardButton(text='Обновить', callback_data=f'refresh')
        keyboard = InlineKeyboardMarkup().add(btn1, btn6, btn2).add(btn3).add(btn4).add(btn5)
        return keyboard

    async def manage_channel(self, channel_id):
        if is_required(channel_id):
            btn = InlineKeyboardButton(text='Удалить из списка обязательной подписки❌',
                                       callback_data=f'set_required0+{channel_id}')
        else:
            btn = InlineKeyboardButton(text='Добавить в список обязательной подписки✅',
                                       callback_data=f'set_required1+{channel_id}')
        link = await bot.export_chat_invite_link(chat_id=channel_id)
        btn3 = InlineKeyboardButton(text='Открыть ', url=link)
        btn4 = InlineKeyboardButton(text='Удалить', callback_data=f'delete-channel{channel_id}')
        keyboard = InlineKeyboardMarkup().add(btn3, btn4).add(btn)
        return keyboard


class UserButton():
    def __init__(self, user_id):
        self.user_id = user_id

    def game_btns(self):
        btn1 = InlineKeyboardButton(text='Игры для друзей', callback_data='games1')
        btn2 = InlineKeyboardButton(text='Игры с ботом', callback_data='games2')
        btn3 = InlineKeyboardButton(text='Викторины', callback_data='games3')

        keyboard = InlineKeyboardMarkup().add(btn1, btn2).add(btn3).add(btn)
        return keyboard

    def game1_btns(self):
        btn1 = InlineKeyboardButton(text='Случайные игроки', callback_data='game_id=1-1')
        btn2 = InlineKeyboardButton(text='Правда или действие', callback_data='game_id=1-2')
        btn3 = InlineKeyboardButton(text='Лотерея призов', callback_data='game_id=1-3')

        keyboard = InlineKeyboardMarkup().add(btn1, btn2).add(btn3).add(btn)
        return keyboard

    def game2_btns(self):
        btn1 = InlineKeyboardButton(text='Угадай число', callback_data='game2-1')
        btn2 = InlineKeyboardButton(text='')


def gender_btns():
    male_btn = InlineKeyboardButton(text='Мужской', callback_data='M')
    female_btn = InlineKeyboardButton(text='Женский', callback_data='F')
    cancel_btn = InlineKeyboardButton(text='Отмена', callback_data='break')
    keyboard = InlineKeyboardMarkup().add(male_btn, female_btn).add(cancel_btn)
    return keyboard


def submit_btns():
    submit_btn = InlineKeyboardButton(text='Подтвердить сохранение', callback_data='submit')
    break_btn = InlineKeyboardButton(text='Не сохранять', callback_data='break')
    keyboard = InlineKeyboardMarkup().add(submit_btn).add(break_btn)
    return keyboard


def sign_btns():
    sign_in = InlineKeyboardButton(text='Войти', callback_data='sign-in')
    sign_up = InlineKeyboardButton(text='Зарегистрироваться', callback_data='sign-up')
    keyboard = InlineKeyboardMarkup().add(sign_in).add(sign_up)
    return keyboard


def manage_authors(current_page):
    btn1 = InlineKeyboardButton(text="⬅️", callback_data=f'admin/authors/page={current_page - 1}')
    btn2 = InlineKeyboardButton(text='➡️', callback_data=f'admin/authors/page={current_page + 1}')
    btn3 = InlineKeyboardButton(text='Поиск', callback_data='authors/search')
    keyboard = InlineKeyboardMarkup().add(btn1, btn2).add(btn3)
    return keyboard


def manage_books(current_page, response, count):
    btn1 = InlineKeyboardButton(text="⬅️", callback_data=f'admin/books/page={current_page - 1}')
    btn2 = InlineKeyboardButton(text='➡️', callback_data=f'admin/books/page={current_page + 1}')
    btn3 = InlineKeyboardButton(text='Поиск', callback_data='books/search')
    keyboard = InlineKeyboardMarkup()
    if response['next'] is not None:
        keyboard.add(btn2)
    if response['previous'] is not None:
        keyboard.add(btn1)
    for i in range(1, count):
        keyboard.add(
            InlineKeyboardButton(text=f'Книга номер: {i}', callback_data=f'get_book={int(i)},pag={current_page}'))
    return keyboard


def detail_btns(id):
    btn1 = InlineKeyboardButton(text='Посмотреть', callback_data=f'detail{id}')
    btn2 = InlineKeyboardButton(text='Удалить', callback_data=f'delete{id}')
    keyboard = InlineKeyboardMarkup().add(btn1).add(btn2)
    return keyboard

