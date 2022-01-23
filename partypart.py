import db
import datetime

def message():
    return("привет от бизнес-логики")

def init():
    db.create_table(id)

def add_user(user):
    db.add_user(user)


# datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def _get_now_formatted() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    """Возвращает сегодняшний datetime с учётом времненной зоны Мск."""
    tz = pytz.timezone("Europe/Moscow")
    now = datetime.datetime.now(tz)
    return now
