games = {'1-2': 'Правда или действие', '1-1': "Случайные игроки"}

from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.inline.main_btns import UserButton
from loader import dp, bot


@dp.message_handler(Text(contains='Развлечения'))
async def entertainment(msg: Message):
    await msg.answer('Время для развлечений😁\n'
                     'Выберите один из вариантов!', reply_markup=UserButton(msg.from_user.id).game_btns())


@dp.callback_query_handler(text='games1')
async def answer(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Игры для друзей',
                           reply_markup=UserButton(call.from_user.id).game1_btns())


@dp.callback_query_handler(text='games2')
async def answer(call: CallbackQuery):
    await call.answer('Этот режим игр находится в разработке!', show_alert=True)


@dp.callback_query_handler(text='games3')
async def answer(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Викторины')
