from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default.admin import AdminKeyboard
from utils.db_api.manage import ManageUser


def button(text, data, func):
    kb = InlineKeyboardButton(text=text, callback_data=func + data)
    keyboard = InlineKeyboardMarkup().add(kb)
    return keyboard


def keyboards(list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*list)
    return keyboard


dict = {'btn1': 1, 'btn2': 2, 'btn3': 3}
