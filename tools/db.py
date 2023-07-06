import sqlite3

db = sqlite3.connect('database.db')
cur = db.cursor()


async def db_create():
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "tg_id INTEGER"
                "cart_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS items("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT"
                "desc TEXT"
                "price TEXT"
                "photo TEXT"
                "brand TEXT)")
    db.commit()


async def cmd_start_db(user_id):
    user = cur.execute("SELECT * FROM accounts WHERE tg_id == {key}".format(key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO accounts (tg_id) VALUES ({key})".format(key=user_id))
        db.commit()
