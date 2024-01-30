from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterUser(StatesGroup):
    get_phone = State()
    get_language = State()
    sign = State()
    sign_in = State()
    sign_up = State()
    get_username = State()
    get_password = State()



class Chat(StatesGroup):
    get_public_msg = State()
    get_private_msg_to_user = State()
    get_private_msg_to_admin = State()
    get_message_to_answer = State()
    get_public_msg_to_edit = State()
    get_private_msg_to_edit = State()
    get_id_to_search = State()
    edit_public_msgs = State()
    edit_private_msg = State()

class ChannelState(StatesGroup):
    get_title = State()
    get_id = State()

class Weather(StatesGroup):
    get_location = State()


class AuthorCreateState(StatesGroup):
    get_name = State()
    get_age = State()
    get_gender = State()
    get_bio = State()
    finish = State()



class GameSession(StatesGroup):
    get_question = State()
    get_mission = State()


class NoteSession(StatesGroup):
    get_title = State()
    get_text = State()


class myPlanStates(StatesGroup):
    get_title = State()
    get_text = State()
    get_type = State()
    get_deadline = State()
