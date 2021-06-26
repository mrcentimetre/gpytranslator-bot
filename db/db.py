import sqlite3


db = sqlite3.connect("userlanguages.db")
dbc = db.cursor()
dbc.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id BIGINT PRIMARY KEY,
    chat_lang
)""")
db.commit()
