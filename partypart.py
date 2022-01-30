from datetime import datetime
import re
from typing import List, NamedTuple, Optional

import db
import exceptions


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""
    amount: int
    user_name: str


class Expense(NamedTuple):
    """Структура добавленного в БД нового расхода"""
    id: Optional[int]
    amount: int
    user_name: str


def init():
    db.create_table(id)


def add_expense(raw_message: str, owner) -> Expense:
    parsed_message = _parse_message(raw_message)
    sql = db.get_cursor()
    sql.execute(f'INSERT INTO expenses (owner, user, expense, date) VALUES(?, ?, ?, ?)', (owner, parsed_message.user_name, parsed_message.amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    db.base.commit()
    # print(str(owner) + " " + parsed_message.user_name + " " + parsed_message.amount + " added.")        
    return Expense(id=None, amount=parsed_message.amount, user_name=parsed_message.user_name)

def total(owner):
    sql = db.get_cursor()
    answer = sql.execute(f'SELECT id, user, sum(expense) FROM expenses WHERE owner = (?) GROUP BY user', (str(owner),))
    rows = answer.fetchall()
    total_expenses = [Expense(id=row[0], user_name=row[1], amount=row[2]) for row in rows]
    print(total_expenses)
    return total_expenses


    # rows = cursor.fetchall()
    # last_expenses = [Expense(id=row[0], amount=row[1], category_name=row[2]) for row in rows]

# def get_today_statistics() -> str:
#     """Возвращает строкой статистику расходов за сегодня"""
#     cursor = db.get_cursor()
#     cursor.execute("select sum(amount)"
#                    "from expense where date(created)=date('now', 'localtime')")
#     result = cursor.fetchone()
#     if not result[0]:
#         return "Сегодня ещё нет расходов"
#     all_today_expenses = result[0]
#     cursor.execute("select sum(amount) "
#                    "from expense where date(created)=date('now', 'localtime') "
#                    "and category_codename in (select codename "
#                    "from category where is_base_expense=true)")
#     result = cursor.fetchone()
#     base_today_expenses = result[0] if result[0] else 0
#     return (f"Расходы сегодня:\n"
#             f"всего — {all_today_expenses} руб.\n"
#             f"базовые — {base_today_expenses} руб. из {_get_budget_limit()} руб.\n\n"
#             f"За текущий месяц: /month")


# SELECT user, sum(expense) FROM expenses WHERE owner = 197902523 GROUP BY user

# SELECT author, SUM(price * amount) AS Стоимость
# FROM book -- Вывести суммарную стоимость книг каждого автора.
# GROUP BY author;

    # cursor.execute(f"select sum(amount) "
    #                f"from expense where date(created) >= '{first_day_of_month}' "
    #                f"and category_codename in (select codename "
    #                f"from category where is_base_expense=true)")



def _parse_message(raw_message: str) -> Expense:
    """Парсит текст пришедшего сообщения о новом расходе."""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n800 Сергей")

    amount = regexp_result.group(1).replace(" ", "")
    user_name = regexp_result.group(2).strip()
    return Message(amount=amount, user_name=user_name)

def user():
    pass


def amount():
    pass



# datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(tz)
    return now
