from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from handlers.admins.office_tools import myNotes, myPlans, filterPlansJson

btn = InlineKeyboardButton(text='Назад', callback_data='admin/back')
remove_btn = InlineKeyboardButton(text='❌', callback_data='remove-btn')
deleteNotes = InlineKeyboardButton(text='Удалить заметки', callback_data='notes/delete')
filterPlans = InlineKeyboardButton(text='Фильтровать', callback_data='admin/plans/filter-mode=True')
dontFilter = InlineKeyboardButton(text='Не фильтровать', callback_data='admin/plans/filter-mode=False')
add_notes = InlineKeyboardButton(text='Добавить заметки', callback_data='notes/new')
add_plans = InlineKeyboardButton(text='Добавить планы', callback_data='plans/new')


def mainSwitchBtns(page):
    pre_btn = InlineKeyboardButton(text='⬅️', callback_data=f'plans/switch-pre-page/{page}')
    next_btn = InlineKeyboardButton(text='➡️', callback_data=f'plans/switch-next-page/{page}')
    buttons = [pre_btn, remove_btn, next_btn]
    return buttons


def myCabinetBtn(message_id=None):
    remove_btn = InlineKeyboardButton(text='❌', callback_data=f'remove-btn{message_id}')
    btn1 = InlineKeyboardButton(text='Мои пароли', callback_data='admin/my-passwords')
    btn2 = InlineKeyboardButton(text='Профиль', callback_data='admin/profile')
    btn3 = InlineKeyboardButton(text='Заметки', callback_data='admin/notes')
    btn4 = InlineKeyboardButton(text='Планы', callback_data='admin/plans')
    keyboard = InlineKeyboardMarkup().add(btn1, btn2).add(btn3, btn4).add(remove_btn)
    return keyboard


def myNotesBtn(page=1, function='see', msg_id=None):
    # Получаем заметки в json формате
    notes = myNotes().list(page=page)
    remove_btn = InlineKeyboardButton(text='❌', callback_data=f'remove-btn{msg_id}')
    previous_btns = InlineKeyboardButton(text='⬅️', callback_data=f'notes/page/{page - 1}, {function}')
    next_btns = InlineKeyboardButton(text='➡️', callback_data=f'notes/page/{page + 1}, {function}')
    btn_list = [InlineKeyboardButton(text=f'{note["title"]}', callback_data=f'{function}-note/{note["id"]}, {page}') for
                note in
                notes["results"]]

    keyboard = InlineKeyboardMarkup().add(add_notes)
    keyboard2 = InlineKeyboardMarkup().add(*btn_list).add(add_notes, deleteNotes).add(previous_btns, remove_btn,
                                                                                      next_btns)
    if len(btn_list) < 1:
        return False, keyboard
    return True, keyboard2


def myPlansBtn(page=None, filterMode=False):
    if page is None:
        page = f'page=1'
    plans, text, get_status = filterPlansJson(page)
    if not get_status:
        return False, InlineKeyboardMarkup().add(add_plans), text
    typesList = myPlans().types_list()
    switch_buttons = mainSwitchBtns(page)
    btnList = [
        InlineKeyboardButton(text=f'{plan["title"]}', callback_data=f'admin/plan-detail/{plan["id"]}, {page}, get')
        for plan
        in plans]
    typesBtnList = [InlineKeyboardButton(text=f'{type[1]}', callback_data=f'admin/plans/filter/{page}&type={type[0]}')
                    for type
                    in
                    typesList]
    typesBtnList.append(
        InlineKeyboardButton(text=f'Завершённые', callback_data=f'admin/plans/filter/{page}&status={True}'))
    typesBtnList.append(
        InlineKeyboardButton(text=f'Не завершённые', callback_data=f'admin/plans/filter/page={page}&status={False}'))

    keyboard2 = InlineKeyboardMarkup().add(*btnList).add(add_plans, filterPlans).add(
        *switch_buttons)
    keyboard3 = InlineKeyboardMarkup().add(*typesBtnList).add(dontFilter).add(remove_btn)
    if filterMode:
        return True, keyboard3, text
    return True, keyboard2, text


def setPlanStatus_kb(current_status, pk):
    if current_status:
        status = False
        text = 'Отменить выполнение➖'
    else:
        status = True
        text = 'Выполнено✅'
    btn = InlineKeyboardButton(text=text, callback_data=f'admin/plans/set-status/{pk}+{status}')
    return InlineKeyboardMarkup().add(remove_btn, btn)
