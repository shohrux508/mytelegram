import asyncio
import time

import requests as r
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from handlers.entertainment.tools import generate_join_link, generate_game_code, sessions, SessionManager, \
    get_users_list_as_text, find_game_by_user_id, get_qm_list_as_text, SentMessagesManager
from keyboards.inline.game_btns import start_game_btn, manage_game_creator, mission_manager, add_another, \
    manage_game_player
from keyboards.one_time_keyboards import button
from loader import dp, bot
from shortcuts.game_shortcuts import send_msg_all, edit_msg_all
from shortcuts.main_shortcuts import filter_data
from states.StatesGroup import GameSession


@dp.callback_query_handler(text='game_id=1-2')
async def answer(call: CallbackQuery, state: FSMContext):
    game = 'Правда или действие'
    response = r.get(url='http://127.0.0.1:8000/myserver/chat-games/1/')
    if response.status_code != 200:
        await call.answer('Игра не доступна!')
        return
    rules = (response.json())['rules']
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=rules,
                                reply_markup=start_game_btn('game_id=1-2'))


@dp.callback_query_handler(lambda x: x.data and 'create' in x.data and 'game_id=1-2' in x.data)
async def create_session(call: CallbackQuery):
    code = generate_game_code(call.from_user.id)
    SessionManager(code).create(code, call.from_user.id)
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Вы создали игру: Правда или действие.\n'
                                     'Вы можете управлять за процессом игры:\n'
                                     'также начинать и завершать игру',
                                reply_markup=manage_game_creator(call.from_user.id, status=False))


@dp.callback_query_handler(text='start-game')
async def start_game(call: CallbackQuery):
    game_code = find_game_by_user_id(call.from_user.id)
    await send_msg_all(game_code, [call.from_user.id], 'Игра началась', save_id=False, keyboard=manage_game_player())
    await send_msg_all(game_code, [], '...', save_id=True, keyboard=False)
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Игра началась',
                                reply_markup=manage_game_creator(call.from_user.id, status=True))
    time.sleep(1)
    for i in range(0, 3):
        await edit_msg_all(game_code, [], message_txt=f'Выбираем пользователя...{i}', keyboard=False)
        time.sleep(1)
    user_id, name, count = SessionManager(game_code).choose_player()
    qm = SessionManager(game_code).choose_qm()

    await edit_msg_all(game_code, [user_id], message_txt=f'{count}.Участник выбран!',
                       keyboard=button('Смотреть', f'{user_id}+{name}+{qm}', 'see-user='))
    message_id = SentMessagesManager(game_code).get_message_id(user_id)
    await bot.edit_message_text(chat_id=user_id, message_id=message_id, text='Мы выбрали вас случайным образом!',
                                reply_markup=button('Смотреть задание', f'{user_id}+{name}+{qm}', 'see-user='))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('see-user'))
async def see_user(call: CallbackQuery):
    data = filter_data(call.data, 'see-user=')
    user_id, name, qm = data.split('+')
    if user_id == call.from_user.id:
        await call.answer(f'Задание: {qm}', show_alert=True)
        return
    await call.answer(f'Участник: {user_id}\n'
                      f'Имя: {name}\n'
                      f'Задание: {qm}', show_alert=True)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('finish-game='))
async def finish_game_h(call: CallbackQuery):
    game_code = filter_data(call.data, 'finish-game=')
    st = SessionManager(game_code).delete()
    if st[0] == True:
        for id in st[1]:
            if id == call.from_user.id:
                continue
            await bot.send_message(chat_id=id, text='Игра завершена!')
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text=f'Игра {game_code} завершена!')
        return
    await call.answer('Не удалось завершить игру!')


@dp.callback_query_handler(lambda x: x.data and 'see-users-list=' in x.data)
async def get_list(call: CallbackQuery):
    game_code = filter_data(call.data, 'see-users-list=')
    text = get_users_list_as_text(game_code)
    await call.answer(text, show_alert=True)


@dp.callback_query_handler(lambda x: x.data and 'add-question' in x.data)
async def add_question(call: CallbackQuery, state: FSMContext):
    plus = False
    if '+' in call.data:
        plus = True
    message = await bot.send_message(chat_id=call.from_user.id, text='Напишите ваш вопрос: \n'
                                                                     'Отменить: /break')
    await state.update_data(msg_id=message.message_id, plus=plus)
    await state.set_state(GameSession.get_question.state)


@dp.message_handler(state=GameSession.get_question.state)
async def get_question(msg: Message, state: FSMContext):
    data = await state.get_data()
    msg_id = data.get("msg_id")
    plus = data.get('plus')
    if 'break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg_id)
        return
    question = msg.text
    game_code = find_game_by_user_id(msg.from_user.id)
    status = SessionManager(game_code).add_question(question)
    if status:
        if plus:
            await bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg_id, text='Вопрос добавлен!',
                                        reply_markup=add_another(type='question'))
        else:
            await bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg_id, text='Вопрос добавлен!',
                                        reply_markup=button('Добавить задание', '', 'add-mission'))
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    else:
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg_id, text='Не удалось добавить!')


@dp.callback_query_handler(lambda x: x.data and 'add-mission' in x.data)
async def add_mission(call: CallbackQuery, state: FSMContext):
    plus = False
    if '+' in call.data:
        plus = True
    message = await bot.send_message(chat_id=call.from_user.id, text='Напишите текст задания: \n'
                                                                     'Отменить: /break')
    await state.update_data(message_id=message.message_id, plus=plus)
    await state.set_state(GameSession.get_mission.state)


@dp.message_handler(state=GameSession.get_mission.state)
async def get_mission(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    plus = (await state.get_data()).get('plus')
    if 'break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
        return
    game_code = find_game_by_user_id(msg.from_user.id)
    status = SessionManager(game_code).add_mission(mission=msg.text)
    if status:
        if plus:
            await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Задание добавлено!',
                                        reply_markup=add_another(type='mission'))
        else:
            await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Задание добавлено!')
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    else:
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Не удалось добавить!')


@dp.callback_query_handler(text='manage-qm')
async def manage_qm(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Вопросы/Задания',
                                reply_markup=mission_manager())


@dp.callback_query_handler(text='main')
async def main(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Главная',
                                reply_markup=manage_game_creator(call.from_user.id, True))


@dp.callback_query_handler(lambda x: x.data and 'see-qm' in x.data)
async def see_questions(call: CallbackQuery):
    if 'questions' in call.data:
        type = 'questions'
    else:
        type = 'missions'
    game_code = find_game_by_user_id(call.from_user.id)
    text = get_qm_list_as_text(game_code, type)
    await call.answer(text, show_alert=True)


@dp.callback_query_handler(text='clear-qm')
async def clear_qm(call: CallbackQuery):
    game_code = find_game_by_user_id(call.from_user.id)
    SessionManager(game_code).clear_qm()
    await call.answer('Очищено!')


@dp.callback_query_handler(text='next-gamer')
async def next_(call: CallbackQuery):
    game_code = find_game_by_user_id(call.from_user.id)
    await send_msg_all(game_code, [], '...', save_id=True, keyboard=False)

    time.sleep(1)
    for i in range(0, 3):
        await edit_msg_all(game_code, [], message_txt=f'Выбираем пользователя...{i}', keyboard=False)
        time.sleep(1)
    user_id, name, count = SessionManager(game_code).choose_player()
    qm = SessionManager(game_code).choose_qm()

    await edit_msg_all(game_code, [user_id], message_txt=f'{count}.Участник выбран!',
                       keyboard=button('Смотреть', f'{user_id}+{name}+{qm}', 'see-user='))
    message_id = SentMessagesManager(game_code).get_message_id(user_id)
    await bot.edit_message_text(chat_id=user_id, message_id=message_id, text='Мы выбрали вас случайным образом!',
                                reply_markup=button('Смотреть задание', f'{user_id}+{name}+{qm}', 'see-user='))


@dp.callback_query_handler(text='users-list')
async def user_list(call: CallbackQuery):
    game_code = find_game_by_user_id(call.from_user.id)
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text=get_users_list_as_text(game_code), reply_markup=button('Назад', '', 'back-btn'))


@dp.callback_query_handler(text='back-btn')
async def back_h(call: CallbackQuery):
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Игра: Правда и Действие.',
                                reply_markup=manage_game_player())
