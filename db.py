import sqlite3

base = sqlite3.connect("patrypart.db", check_same_thread=False)
sql = base.cursor()


def delete(row_id: int) -> None:
    row_id = int(row_id)
    sql.execute(f"delete from expenses where id=(?)", (row_id,))
    base.commit()


def restart(owner):
    sql.execute(f"delete from expenses where owner=(?)", (owner,))
    base.commit()


def get_cursor():
    return sql


def check_db_exists():
    """Проверяет наличие основной таблицы, если её нет - создаёт"""
    sql.execute("""CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT,
            user TEXT,
            expense INTEGER,
            comment TEXT,
            date timestamp)""")
    base.commit()

check_db_exists()