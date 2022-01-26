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
