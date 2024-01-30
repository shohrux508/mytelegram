import datetime

from data.config import ADMINS
from data.database import *


def create_id(table, id_index):
    cur.execute(f"""SELECT * FROM {table}""")
    result = cur.fetchall()
    id_index = int(id_index)
    if result == []:
        id = 1
    else:
        id = result[-1][id_index] + 1
    return id


def search_user(phone_or_id: str or int):
    id = phone_or_id
    if "+" not in id:
        user = ManageUser(id).get(by=False, table_name='', data='')
    else:
        user = ManageUser(id).get(by=True, table_name='phone', data=id)
    if user is None:
        return False
    else:
        if user[1]:
            status = 'Заблокирован'
        else:
            status = 'Имеет доступ к боту'
        if user[2]:
            pos = 'Администратор'
        else:
            pos = 'Пользователь'
        text = (f'{pos}-{user[3]}: {user[6]}\n'
                f'Идентификационный номер: {user[0]}\n'
                f'Статус: {status}\n'
                f'Дата присоединения: {user[5]}\n'
                f'Номер телефона: {user[4]}')
        response = [user[0], text]

        return response


class ManageUser():
    def __init__(self, user_id):
        self.user_id = user_id

    def new(self, full_name, phone, is_admin, is_blocked, language, token):
        if str(self.user_id) in ADMINS:
            is_admin = 3
        id = create_id(table='users', id_index='6')
        now = datetime.datetime.now().strftime("%D(%H:%M:%S)")
        cur.execute(
            f'''INSERT INTO users VALUES('{self.user_id}', '{is_blocked}', '{is_admin}', '{full_name}', '{phone}', '{now}', '{id}', '{language}', '{token}')''')
        conn.commit()
        return ()
    def auth_token(self):
        cur.execute(f'''SELECT auth_token FROM users WHERE user_id = "{self.user_id}" ''')
        auth_token = cur.fetchone()
        return auth_token

    def get(self, by: bool, table_name: str, data: str or int):
        if by:
            cur.execute(f'''SELECT * FROM users WHERE {table_name} = "{data}" ''')
        else:
            cur.execute(f'''SELECT * FROM users WHERE user_id = {self.user_id}''')
        user = cur.fetchone()
        return user

    def block(self, status):
        cur.execute(f'''UPDATE users SET is_blocked = '{status}' WHERE user_id = {self.user_id}''')
        conn.commit()

        return ()

    def admin(self, position):
        cur.execute(f'''UPDATE users SET is_admin = '{position}' WHERE user_id = {self.user_id} ''')
        conn.commit()
        return ()

    def list(self, select_id, filter_by, period):
        if filter_by == 'admin':
            cur.execute(f'''SELECT * FROM users WHERE is_admin > 0''')
        elif filter_by == 'blocked':
            cur.execute(f'''SELECT * FROM users WHERE is_blocked != 0''')
        else:
            cur.execute(f'''SELECT * FROM users''')

        users = cur.fetchall()
        list = []
        if select_id:
            for user in users:
                list.append(user[0])

        else:
            list = users

        if period:
            start = int(period[0])
            end = int(period[1])
            list = list[start:end]

        return list

    def is_user(self):
        cur.execute(f'''SELECT * FROM users WHERE user_id = '{self.user_id}' ''')
        user = cur.fetchone()
        if user is None:
            return False
        else:
            return True

    def is_admin(self):
        cur.execute(f'''SELECT is_admin FROM users WHERE user_id = {self.user_id}''')
        response = cur.fetchone()
        if response is None:
            return False
        elif response[0] > 0:
            return True
        else:
            return False

    def is_blocked(self):
        cur.execute(f'''SELECT is_blocked FROM users WHERE user_id = '{self.user_id}' ''')
        response = cur.fetchone()
        if response is None:
            return False
        elif response[0] != 0:
            return True
        else:
            return False








class Channel():

    def __init__(self, user_id):
        self.user_id = user_id

    def create(self, channel_id, name, is_required):
        cur.execute(f'''INSERT INTO channels VALUEs('{channel_id}', '{self.user_id}', '{name}', '{is_required}');''')
        conn.commit()
        return id

    def get(self, channel_id):
        cur.execute(f'''SELECT * FROM channels WHERE channel_id = "{channel_id}"''')
        channel = cur.fetchone()
        return channel

    def remove(self, channel_id):
        cur.execute(f'''DELETE FROM channels WHERE channel_id = "{channel_id}" ''')
        conn.commit()
        print(f'removed{channel_id}')
        return True

    def list(self):
        cur.execute(f'''SELECT * FROM channels''')
        list = cur.fetchall()
        return list

    def set_required(self, status: int, channel_id: int):
        cur.execute(f'''UPDATE channels SET is_required = {status} WHERE channel_id = {channel_id}''')
        conn.commit()
        return True

    def get_required_channels(self):
        cur.execute(f"""SELECT * FROM channels WHERE is_required = 1""")
        channels = cur.fetchall()
        return channels
