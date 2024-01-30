from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.entertainment.tools import game_codes, generate_join_link, find_game_by_user_id, SessionManager

btn = InlineKeyboardButton(text='❌', callback_data='remove-btn')




def start_game_btn(game_id):
    btn1 = InlineKeyboardButton(text='Создать игру', callback_data=f'create, {game_id}')
    btn2 = InlineKeyboardButton(text='Присоединиться к игре', callback_data=f'join, {game_id}')
    keyboard = InlineKeyboardMarkup().add(btn1, btn2).add(btn)
    return keyboard


def manage_game_creator(user_id, status):
    game_code = game_codes[user_id]
    link = generate_join_link(game_code)
    btn1 = InlineKeyboardButton(text='Пригласить друзей', switch_inline_query=link)
    btn2 = InlineKeyboardButton(text='Завершить игру', callback_data=f'finish-game={game_code}')
    btn3 = InlineKeyboardButton(text='Начать игру', callback_data=f'start-game')
    btn4 = InlineKeyboardButton(text='Вопросы/задания', callback_data=f'manage-qm')
    btn5 = InlineKeyboardButton(text='Посмотреть список участников', callback_data=f'see-users-list={game_code}')
    btn6 = InlineKeyboardButton(text='Следующий участник', callback_data='next-gamer')
    keyboard = InlineKeyboardMarkup().add(btn3, btn4).add(btn5, btn1)
    keyboard2 = InlineKeyboardMarkup().add(btn2, btn4).add(btn5, btn6)
    if status:
        return keyboard2
    return keyboard

def mission_manager():
    btn1 = InlineKeyboardButton(text='Все вопросы', callback_data='see-qm-questions')
    btn2 = InlineKeyboardButton(text='Все задания', callback_data='see-qm-missions')
    btn3 = InlineKeyboardButton(text='Добавить вопрос', callback_data='add-question+')
    btn4 = InlineKeyboardButton(text='Добавить задание', callback_data='add-mission+')
    btn5 = InlineKeyboardButton(text='Очистить', callback_data='clear-qm')
    btn6 = InlineKeyboardButton(text='Назад', callback_data='main')
    keyboard = InlineKeyboardMarkup().add(btn1, btn2).add(btn3, btn4).add(btn5).add(btn6)
    return keyboard
def manage_game_player():
    btn1 = InlineKeyboardButton(text='Список участников', callback_data=f'users-list')
    btn2 = InlineKeyboardButton(text='Написать создателю', callback_data=f'send_message, creator')
    btn3 = InlineKeyboardButton(text='Покинуть игру', callback_data=f'quit_game')
    keyboard = InlineKeyboardMarkup().add(btn1).add(btn2).add(btn3)
    return keyboard


def add_another(type):
    if type == 'question':
        btn1 = InlineKeyboardButton(text='Добавить ещё', callback_data='add-question+')
    else:
        btn1 = InlineKeyboardButton(text='Добавить ещё', callback_data='add-mission+')
    keyboard = InlineKeyboardMarkup().add(btn1).add(btn)
    return keyboard

def gamer_view():
    btn1 = InlineKeyboardButton(text='Смотреть задание', callback_data='see-user=')
    btn2 = InlineKeyboardButton(text='Ответить/Выполнить ✅', callback_data='done')
