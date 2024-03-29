import telebot

import partypart
from config import admin_id, token


def telegram_bot(token):
    bot = telebot.TeleBot(token)


# Выводит приветственное сообщение
    @bot.message_handler(commands=['start', 'help'])
    def start_message(message):
        partypart.add_user_name(message)
        bot.send_message(message.chat.id, "Добро пожаловать в PartyPart\n\n"
                                          "Вызвать эту справку /help или /start\n"
                                          "Получить подробную справку о работе бота /info\n"
                                          "Для добавления трат внесите данные в формате – Сумма Имя.\nНапример – 500 Сергей)\n"
                                          "Удалить запись о расходах /del + номер записи\n"
                                          "Посмотреть список всех трат /show_all\n"
                                          "Посмотреть итоги /total\n"
                                          "Удалить все записи о мероприятии /restart")


# Выводит справку о предназначении бота
    @bot.message_handler(commands=['info'])
    def info_message(message):
        bot.send_message(message.chat.id, "PartyPart – бот для учета расходов на мероприятие.\n\n"
                                          "Предположим, вы с друзьями решили устроить вечеринку:\n"
                                          "– Андрей купил вино за 1050 рублей и мандарины за 240\n"
                                          "– Пётр купил сыр за 500 и виноград за 370\n"
                                          "– Анна заказала суши за 1450\n"
                                          "– Вероника выбрала пиццу за 560\n"
                                          "– Сергей опаздывал на мероприятие и не успел купить ничего\n"
                                          "Вы вносите все эти траты в бота и он рассчитывает кому надо докинуть денег, а кому забрать из общего банка.")


# Вывод списка всех трат
    @bot.message_handler(commands=['show_all'])
    def show_all(message):
        all_expenses = partypart.show_all(message.chat.id)
        all_expenses_rows = [
            f"{expense.user_name} – {expense.amount}.         /del{expense.id}\n"
            for expense in all_expenses
        ]
        answer_message = "Список расходов: (/del – удалить запись)\n\n" + "".join(all_expenses_rows)
        bot.send_message(message.chat.id, answer_message)


# Вывод статистики
    @bot.message_handler(commands=['total'])
    def total_message(message):
        total_expenses = partypart.total(message.chat.id)
        total_expenses_rows = [
            f"{expense.user_name} – {expense.amount}. {' Необходимо внести ' if expense.debt > 0 else ' Нужно получить '} {abs(expense.debt)}\n"
            for expense in total_expenses
        ]
        answer_message = "Вклад в общие расходы:\n\n" + "".join(total_expenses_rows)
        bot.send_message(message.chat.id, answer_message)


# Перезапуск мероприятия / удаление всех записей
    @bot.message_handler(commands=['restart', 'clear_all'])
    def restart(message):
        answer_message = partypart.clear_all(message.chat.id)
        bot.send_message(message.chat.id, answer_message)


# Админ. Вывод информации о доступных командах
    @bot.message_handler(commands=['admin'])
    def admin_info(message):
        if message.chat.id == admin_id:
            bot.send_message(message.chat.id, "Доступны следующие команды: \n\n"
                                              "Проверить список уникальных пользователей – /show_unique_users\n"
                                              "Просмотреть список всех записей в базе – /admin_show_all\n"
                                              "Удалить все записи из базы – /sudo_restart\n"
                                              "Проверка имени - /say_my_name\n")


# Админ. Вывод всех записей в базе
    @bot.message_handler(commands=['admin_show_all'])
    def admin_show_all(message):
        if message.chat.id == admin_id:
            all_expenses = partypart.admin_show_all()
            all_expenses_rows = [
                f"{expense.user_name} – {expense.amount}.         /admin_del{expense.id}\n"
                for expense in all_expenses
            ]
            answer_message = "Список расходов: (/admin_del – удалить запись)\n\n" + "".join(all_expenses_rows)
            bot.send_message(message.chat.id, answer_message)


# Поиск имени пользователя
    @bot.message_handler(commands=['say_my_name'])
    def say_my_name(message):
        answer_message = message.chat.username
        bot.send_message(message.chat.id, answer_message)


# Админ. Отображения всех уникальных пользователей
    @bot.message_handler(commands=['show_unique_users'])
    def show_unique_users(message):
        if message.chat.id == admin_id:
            users = partypart.show_unique_users()
            users_rows = [f"{user}.\n" for user in users]
        answer_message = "Список уникальных пользователей\n\n" + "".join(users_rows)
        bot.send_message(message.chat.id, answer_message)


# Админ. Перезапуск всей базы
    @bot.message_handler(commands=['sudo_restart'])
    def sudo_restart(message):
        if message.chat.id == admin_id:
            answer_message = partypart.sudo_restart()
            bot.send_message(message.chat.id, answer_message)


# Добавление и удаление трат – удаление записей по id, парсинг сообщения и сохранение данных в таблицу
    @bot.message_handler()
    def add_expense(message):
        if (message.text.startswith('/del')):
            '''Удаляем запись по её номеру в базе данных'''
            try:
                row_id = int(message.text[4:])
                answer_message = partypart.delete_expense(message.chat.id, row_id)
                bot.send_message(message.chat.id, answer_message)
            except Exception:
                bot.send_message(message.chat.id, 'Введите команду в формате /delX, где Х - номер записи о затратах')
                return
        elif (message.text.startswith('/admin_del')):
            if message.chat.id == admin_id:
                try:
                    row_id = int(message.text[10:])
                    answer_message = partypart.admin_delete_expense(row_id)
                    bot.send_message(message.chat.id, answer_message)
                except Exception:
                    bot.send_message(message.chat.id,
                                    'Введите команду в формате /admin_delX, где Х - номер записи о затратах')
                    return
        else:
            try:
                expense = partypart.add_expense(message.text, message.chat.id)
            except Exception as e:
                bot.send_message(message.chat.id, e)
                return
            answer_message = (
                f"Добавлены траты от {expense.user_name} на сумму {expense.amount}.\n\n"
                f"Посмотреть весь список трат – /show_all\n"
                f"Посмотреть текущие итоги – /total")
            bot.send_message(message.chat.id, answer_message)

    bot.polling()


if __name__ == '__main__':
    print('Бот запущен')
    telegram_bot(token)
