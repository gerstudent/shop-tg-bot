import sqlite3

db = sqlite3.connect('database.db')
cur = db.cursor()


async def db_create():
    cur.execute("CREATE TABLE IF NOT EXISTS accounts("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "cart_id TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS items("
                "i_id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "name TEXT"
                "desc TEXT"
                "price TEXT"
                "photo TEXT"
                "brand TEXT)")
    db.commit()
