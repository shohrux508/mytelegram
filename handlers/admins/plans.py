from aiogram.types import CallbackQuery

from handlers.admins.office_tools import switchPage_datas, myPlans, getPlanText
from keyboards.inline.office_keyboards import myPlansBtn, setPlanStatus_kb
from loader import dp, bot
from shortcuts.main_shortcuts import filter_data


@dp.callback_query_handler(text='admin/plans')
async def my_plans(call: CallbackQuery):
    if myPlansBtn()[0] == False:
        plans = 'Пусто'
    else:
        plans = 'Ваши планы'
    await bot.send_message(chat_id=call.from_user.id, text=plans, reply_markup=myPlansBtn()[1])
    return


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('admin/plans/filter-mode'))
async def filterMode(call: CallbackQuery):
    status = filter_data(call.data, 'admin/plans/filter-mode=')
    if status == 'True':
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Фильтровать',
                                    reply_markup=myPlansBtn(filterMode=True)[1])
        return
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Ваши планы',
                                reply_markup=myPlansBtn()[1])
    return


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('plans/switch'))
async def switchPage(call: CallbackQuery):
    data = filter_data(call.data, 'plans/switch-')
    if 'next' in data:
        current_page = filter_data(data, 'next-page/')
        switch_page = switchPage_datas(current_page, next=True)
    elif 'pre' in data:
        current_page = filter_data(data, 'pre-page/')
        switch_page = switchPage_datas(current_page, previous=True)
    else:
        switch_page = None
    if switch_page:
        if not myPlansBtn(page=switch_page)[0]:
            await call.answer('Неправильная страница!')
            return
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text=myPlansBtn(page=switch_page)[2],
                                    reply_markup=myPlansBtn(page=switch_page)[1])
    return


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('admin/plans/filter/'))
async def filterPlans(call: CallbackQuery):
    page = filter_data(call.data, 'admin/plans/filter/')
    if myPlansBtn(page=page)[0] == False:
        return
    st, keyboard, text = myPlansBtn(page=page)
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                reply_markup=keyboard)
    return


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('admin/plan-detail/'))
async def seePlan(call: CallbackQuery):
    pk, page, method = (filter_data(call.data, 'admin/plan-detail/')).split(',')
    message, status = getPlanText(pk)
    await bot.send_message(chat_id=call.from_user.id, text=message,
                           reply_markup=setPlanStatus_kb(current_status=status, pk=pk))
    return


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('admin/plans/set-status/'))
async def setStatus(call: CallbackQuery):
    pk, status = filter_data(call.data, 'admin/plans/set-status/', split_key='+')
    response = myPlans().put(pk=pk, status=status)
    message, status = getPlanText(pk)
    if response:
        await call.answer('Успешно!')
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=message,
                                    reply_markup=setPlanStatus_kb(status, pk))
        return
    await call.answer('Не удалось внести изменения!\n'
                      'Попробуйте, позже!')
    return
