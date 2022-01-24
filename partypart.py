import datetime
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
    # user = parsed_message.user_name
    sql = db.get_cursor()
    sql.execute(f'INSERT INTO expenses (owner, user, expense) VALUES(?, ?, ?)', (owner, parsed_message.user_name, parsed_message.amount))
    db.base.commit()
    print(owner + " " + parsed_message.user_name + " " + parsed_message.amount + " added.")        
    return Expense(id=None, amount=parsed_message.amount, user_name=parsed_message.user_name)

# def add_user(user):
#     sql.execute(f'INSERT INTO expenses (owner, participant, income) VALUES(?, ?, ?)', (user, "test", "150"))
#     base.commit()
    


# def add_expense(raw_message: str) -> Expense:
#     """Добавляет новое сообщение.
#     Принимает на вход текст сообщения, пришедшего в бот."""
#     parsed_message = _parse_message(raw_message)
#     category = Categories().get_category(
#         parsed_message.category_text)
#     inserted_row_id = db.insert("expense", {
#         "amount": parsed_message.amount,
#         "created": _get_now_formatted(),
#         "category_codename": category.codename,
#         "raw_text": raw_message
#     })
#     return Expense(id=None,
#                    amount=parsed_message.amount,
#                    category_name=category.name)


def _parse_message(raw_message: str) -> Expense:
    """Парсит текст пришедшего сообщения о новом расходе."""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n700 Сергей")

    amount = regexp_result.group(1).replace(" ", "")
    user_name = regexp_result.group(2).strip()
    return Message(amount=amount, user_name=user_name)


add_expense("1500 Сергей", "3216576")

def user():
    pass


def amount():
    pass






# datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now
