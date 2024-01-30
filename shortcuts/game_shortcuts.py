from handlers.entertainment.tools import SessionManager, SentMessagesManager
from loader import bot, dp


async def edit_msg_all(game_code, ignore, message_txt, keyboard):
    dict = SessionManager(game_code).list(type='players')
    for user_id, name in dict.items():
        if user_id in ignore:
            continue
        message_id = SentMessagesManager(game_code).get_message_id(user_id)
        if keyboard:
            await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=message_txt, reply_markup=keyboard)
        else:
            await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=message_txt)


async def send_msg_all(game_code, ignore, message_txt, save_id, keyboard):
    dict = SessionManager(game_code).list(type='players')
    for user_id, name in dict.items():
        if user_id in ignore:
            continue
        if keyboard:
            message = await bot.send_message(chat_id=user_id, text=message_txt, reply_markup=keyboard)
        else:
            message = await bot.send_message(chat_id=user_id, text=message_txt)
        if save_id:
            SentMessagesManager(game_code).new_message(user_id, message.message_id)
