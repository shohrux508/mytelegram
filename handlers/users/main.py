from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from keyboards.inline.main_btns import UserButton
from loader import dp, bot
from shortcuts.main_shortcuts import send_message_to_admin
from shortcuts.weather_info import get_weather_by_location
from states.StatesGroup import Weather, Chat


@dp.message_handler(Text(contains='Обратная связь'))
async def answer(msg: Message, state: FSMContext):
    message = await msg.answer('Напиши что нибудь!\n'
                               'Отменить: /break')
    await state.update_data(message_id=message.message_id)
    await state.set_state(Chat.get_private_msg_to_admin.state)


@dp.message_handler(state=Chat.get_private_msg_to_admin.state)
async def answer(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if 'break' in msg.text:
        await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
        await state.finish()
        return
    result = await send_message_to_admin(msg)
    if result:
        await msg.answer('Отправлено.')
    else:
        await msg.answer('Сообщение не отправлено!\n'
                         'Возникла ошибка при попытке отправить сообщение.')
    await state.finish()







@dp.message_handler(commands='weather')
async def get_weather_H(msg: Message, state: FSMContext):
    await msg.answer('Поделитесь местоположение: ')
    await state.set_state(Weather.get_location.state)


@dp.message_handler(state=Weather.get_location.state, content_types='location')
async def answer(msg: Message, state: FSMContext):
    longitude = msg.location.longitude
    latitude = msg.location.latitude
    context = get_weather_by_location(latitude, longitude)
    await msg.answer(f'Погода в вашем городе: {context["city"]}\n'
                     f'Подробно: {context["weather"]}'
                     f'Температура: {round(context["temperature"][0])}\n'
                     f'Ощущается как: {round(context["temperature"][1])}\n'
                     f'Скорость ветра: {context["wind"]}м/с')
