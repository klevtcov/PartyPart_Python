import re
from datetime import datetime
from typing import NamedTuple, Optional

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
    debt: Optional[int]


def add_expense(raw_message: str, owner) -> Expense:
    parsed_message = _parse_message(raw_message)
    db.sql.execute(f'INSERT INTO expenses (owner_id, user, expense, date) VALUES(?, ?, ?, ?)', (owner, parsed_message.user_name, parsed_message.amount, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    db.base.commit()
    return Expense(id=None, amount=parsed_message.amount, user_name=parsed_message.user_name, debt=None)


def add_user_name(owner):
    ''' создаём запись о пользователе с временем первого входа '''
    try: 
        db.sql.execute(f'INSERT INTO owners (owner_id, owner_name, date) VALUES(?, ?, ?)', (owner.chat.id, owner.chat.username, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    except Exception:
                return
    db.base.commit()


def show_all(owner):
    answer = db.sql.execute(f'SELECT id, user, expense, date FROM expenses WHERE owner_id = (?) ORDER BY date', (str(owner),))
    rows = answer.fetchall()
    all_expenses = [Expense(id=row[0], user_name=row[1], amount=row[2], debt=None) for row in rows]
    return all_expenses


def admin_show_all():
    answer = db.sql.execute(f'SELECT id, user, expense, date FROM expenses ORDER BY date')
    rows = answer.fetchall()
    all_expenses = [Expense(id=row[0], user_name=row[1], amount=row[2], debt=None) for row in rows]
    return all_expenses


def total(owner):
    answer = db.sql.execute(f'SELECT id, user, sum(expense), ((SELECT sum(expense) FROM expenses WHERE owner_id = (?)) / (SELECT count(DISTINCT user) FROM expenses WHERE owner_id = (?))) FROM expenses WHERE owner_id = (?) GROUP BY user', (str(owner), str(owner), str(owner),))
    rows = answer.fetchall()
    total_expenses = [Expense(id=row[0], user_name=row[1], amount=row[2], debt=row[3]-row[2]) for row in rows]
    return total_expenses


def clear_all(owner):
    try:
        db.restart(owner)
        return ('Бот перезапущен, все данные удалены')
    except Exception as e:
        print(e)
        return ('Нет доступных полей для удаления')


def delete_expense(owner, row_id: int) -> None:
    """Удаляет сообщение по его идентификатору"""
    try:
        take_owner = db.sql.execute(f'SELECT id, owner_id FROM expenses WHERE id=(?)', (row_id,))
        result = take_owner.fetchone()[1]
        if result == str(owner):
            db.delete(row_id)
            return (f'Запись номер {row_id} удалена')
        else:
            return (f'У вас нет записи с номером {row_id}')
    except Exception:
        return (f'У вас нет записи с номером {row_id}')


def admin_delete_expense(row_id: int) -> None:
    """Удаляет сообщение по его идентификатору"""
    db.delete(row_id)
    return (f'Запись номер {row_id} удалена')


def sudo_restart():
    """Удаляет ВСЕ данные из таблицы трат"""
    db.sudo_restart()
    return ('ВСЕ записи из базы удалены')
    


def _parse_message(raw_message: str) -> Expense:
    """Парсит текст пришедшего сообщения о новом расходе."""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не могу понять сообщение. Напишите сообщение в формате, "
            "например:\n800 Сергей")
    amount = regexp_result.group(1).replace(" ", "")
    user_name = regexp_result.group(2).strip().title()
    return Message(amount=amount, user_name=user_name)


# "Админка"
def show_unique_users() -> None:
    answer = db.sql.execute(f'SELECT DISTINCT owner_name FROM owners')
    rows = answer.fetchall()
    users = [row[0] for row in rows]
    return users
