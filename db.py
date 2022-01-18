import sqlite3

base = sqlite3.connect("patrypart.db", check_same_thread=False)
sql = base.cursor()


def add_user(user):
    pass

def insert():
    pass

def show_all():
    pass

def delete_session():
    pass

def delete_record():
    pass

def get_cursor():
    return sql


def check_db_exists():
    """Проверяет наличие основной таблицы, если её нет - создаёт"""
    sql.execute("""CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT,
            participant TEXT,
            income INTEGER)""")
    base.commit()

check_db_exists()