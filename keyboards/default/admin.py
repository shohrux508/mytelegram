from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class AdminKeyboard():
    def main(self):
        kb1 = KeyboardButton(text='Отправить сообщение')
        kb2 = KeyboardButton(text='Пользователи')
        kb3 = KeyboardButton(text='Настройки')
        kb4 = KeyboardButton(text='Мой кабинет')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(kb1, kb2).add(kb3, kb4)
        return keyboard

    def settings(self):
        kb1 = KeyboardButton(text='Каналы')
        kb2 = KeyboardButton(text='Недавние действия')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(kb1).add(kb2)
        return keyboard
