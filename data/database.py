import sqlite3

conn = sqlite3.connect('db.db')
cur = conn.cursor()
cur.execute(
    f'''CREATE TABLE IF NOT EXISTS users (user_id INTEGER, is_blocked INTEGER, is_admin INTEGER, full_name TEXT, phone TEXT, time TEXT, id INTEGER, language TEXT, auth_token TEXT);''')
conn.commit()

cur.execute(
    f'''CREATE TABLE IF NOT EXISTS channels(channel_id INTEGER, user_id INTEGER, name TEXT, is_required INTEGER); ''')
conn.commit()
host = 'https://shohrux1.pythonanywhere.com'

