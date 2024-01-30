from handlers.entertainment.tools import sessions
from keyboards.default.main import StartKeyboard
from keyboards.default.user import share_phone
from keyboards.one_time_keyboards import button
from loader import bot, dp
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, CommandStart
import requests as r
from states.StatesGroup import RegisterUser
from utils.db_api.manage import ManageUser


@dp.message_handler(CommandStart())
async def start(msg: Message, state: FSMContext):
    joined = False
    if msg.get_args():
        print(msg.get_args())
        game_code = msg.get_args().upper()
        if game_code in sessions:
            sessions[game_code]['players'][msg.from_user.id] = msg.from_user.full_name
            await state.update_data(session=game_code)
            joined = True
        else:
            await msg.answer("Игра не найдена.")

    if ManageUser(msg.from_user.id).is_user() == False:
        message = await msg.answer('Поделитесь номером телефона!\n', reply_markup=share_phone())
        await state.update_data(message_id=message.message_id)
        await state.set_state(RegisterUser.get_phone.state)
    else:
        if joined:
            await msg.answer(f"Вы успешно присоединились к игре {game_code}!")
            await msg.answer(f'Для участия в игре вам необходимо добавить минимум один вопрос и одно задание!', reply_markup=button('Добавить вопрос/задание', '', 'add-question'))
        await msg.answer(f'Привет! {msg.from_user.first_name}', reply_markup=StartKeyboard(msg.from_user.id).keyboard())


@dp.message_handler(state=RegisterUser.get_phone.state, content_types=['contact', 'text'])
async def get_phone(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if msg.text:
        phone = msg.text
    else:
        phone = msg.contact.phone_number
    ManageUser(msg.from_user.id).new(full_name=msg.from_user.full_name, phone=phone, is_admin=0, is_blocked=0,
                                     language='ru', token='')
    data = {
        "name": f"{msg.from_user.full_name}",
        "telegram_id": f"{msg.from_user.id}",
        "phone": f"{phone}",
    }
    response = r.post(url='http://127.0.0.1:8000/myserver/users/new/', data=data)
    print(response.json())
    await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
    await msg.answer('Привет!', reply_markup=StartKeyboard(msg.from_user.id).keyboard())
    code = (await state.get_data()).get('session')
    if code is not None:
        await msg.answer(f"Вы успешно присоединились к игре {code}!")
    await state.finish()
