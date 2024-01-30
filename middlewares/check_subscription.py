from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp, bot
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from utils.db_api.manage import Channel
from utils.db_api.check import is_member

keyboards = []
channels_keyboard = None


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            ID = update.message.from_user.id
            if update.message.text in ['/start', '/help']:
                return

        elif update.callback_query:
            ID = update.callback_query.from_user.id
            if update.callback_query.data == f'check+{ID}':
                return
        else:
            return
        result = "Вам необходимо подписаться на каналы чтобы пользоваться ботом:\n"
        final_status = True
        for channel in Channel(user_id=None).get_required_channels():
            channel_id = channel[0]
            status = await is_member(user_id=ID, channel=channel_id)
            final_status *= status
            channel = await bot.get_chat(chat_id=channel_id)

            if not status:
                invite_link = await channel.export_invite_link()
                name = channel.title
                keyboards.append(InlineKeyboardButton(text=name, url=invite_link))
        channels_keyboard = InlineKeyboardMarkup().add(*keyboards)
        if not final_status:
            await update.message.answer(result, disable_web_page_preview=True, reply_markup=channels_keyboard)
            keyboards.clear()
            raise CancelHandler()
