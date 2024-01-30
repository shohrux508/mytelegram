import random
import string

game_codes = {'user_id': 'game_code'}
sessions = {'game_code': {'creator': 1234,
                          'players': {51664346245: 'shohrux', 65122963: 'shohrux_yigitaliev'},
                          'questions': [1, 2, 3, 4, 5],
                          'missions': ['A', 'B', 'C', "D", 'E']}}
sent_messages = {'game_code': {''}}
chosen_players = []
chosen_qms = {'game_code': []}


def find_game_by_user_id(user_id):
    for game_code, game_data in sessions.items():
        if user_id in game_data['players'].keys():
            return game_code
    return None


class SessionManager():
    def __init__(self, game_code):
        self.game_code = game_code

    def create(self, game_code, user_id):
        sessions[game_code] = {}
        sessions[game_code]['creator'] = user_id
        sessions[game_code]['players'] = {user_id: 'Создатель', 1027314278: 'Nilufar', 1795557916: 'name2',
                                          5016643462: 'shohrux', 6512296399: 'shohrux_yigitaliev'}
        sessions[game_code]['questions'] = [1, 2, 3, 4, 5]
        sessions[game_code]['missions'] = ['A', 'B', 'C', 'D', 'E']
        chosen_qms[self.game_code] = []
        print(f'Sessions: {sessions}')
        return True

    def delete(self):
        if self.game_code in sessions:
            list = SessionManager(self.game_code).list(type='players').keys()
            del sessions[self.game_code]
            return True, list
        return False, None

    def choose_player(self):
        while True:
            user = random.choice(list(SessionManager(self.game_code).list(type='players').items()))
            if user[0] not in chosen_players:
                chosen_players.append(user[0])
                return user[0], user[1], len(chosen_players)

    def choose_qm(self):
        while True:
            q_m = random.choice(list(SessionManager(self.game_code).list(type='questions')))
            if q_m not in chosen_qms[self.game_code]:
                chosen_qms[self.game_code].append(q_m)
                return q_m

    def add_question(self, question):
        try:
            sessions[self.game_code]['questions'].append(question)
        except:
            return False
        return True

    def add_mission(self, mission):
        try:
            sessions[self.game_code]['missions'].append(mission)
        except:
            return False
        return True

    def clear_qm(self):
        sessions[self.game_code]['missions'] = []
        sessions[self.game_code]['questions'].clear()
        return True

    def find_creator(self):
        try:
            user_id = sessions[self.game_code]['creator']
        except:
            return False
        return user_id

    def list(self, type):
        try:
            players = sessions[self.game_code][type]
        except:
            return False
        return players

    def join_(self, user_id, name):
        try:
            sessions[self.game_code]['players'][user_id] = name
        except:
            return False
        return True

    def quit_(self, user_id):
        try:
            sessions[self.game_code]['players'].remove(user_id)
        except:
            return False
        return True


class SentMessagesManager():
    def __init__(self, game_code):
        self.game_code = game_code

    def new_message(self, user_id, message_id):
        if self.game_code not in sent_messages.keys():
            sent_messages[self.game_code] = {}

        sent_messages[self.game_code][user_id] = message_id
        return True

    def get_message_id(self, user_id):
        message_id = sent_messages[self.game_code][user_id]
        return message_id


def generate_game_code(user_id):
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if code not in game_codes.values():
            game_codes[user_id] = code
            return code


def generate_join_link(game_code):
    # bot_username = (await bot.me).username
    bot_username = 'shohruxs_bot'
    return f"https://t.me/{bot_username}?start={game_code}"


def get_users_list_as_text(game_code):
    # функция для того что получить список участников игры в готовом формате для отправки сообщения
    dict = SessionManager(game_code).list(type='players')
    full_text = []
    count = 1
    for user_id, name in dict.items():
        text = (f'{count}.{name}: {user_id}')
        full_text.append(text)
        count += 1
    overall_text = '\n\n'.join(full_text)
    return overall_text


def get_qm_list_as_text(game_code, type):
    list = SessionManager(game_code).list(type)
    full_text = []
    count = 1
    for question in list:
        text = (f'{question}')
        full_text.append(text)
        count += 1
    overall_text = '\n\n'.join(full_text)
    return overall_text
