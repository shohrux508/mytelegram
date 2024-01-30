from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



class UserKeyboard():

    def main(self):
        kb1 = KeyboardButton(text='Обратная связь')
        kb2 = KeyboardButton(text='Подробнее обо мне')
        kb3 = KeyboardButton(text='Развлечения 😁')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(kb1).add(kb3, kb2)
        return keyboard

    def settings(self):
        kb1 = KeyboardButton(text='Изменить номер телефона')
        kb2 = KeyboardButton(text='Выйти')
        kb3 = KeyboardButton(text='Сменить язык')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(kb1, kb3).add(kb2)
        return keyboard


def share_phone():
    kb = KeyboardButton(text='Поделиться', request_contact=True)
    return ReplyKeyboardMarkup().add(kb)

