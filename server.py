import telebot
import partypart
from config import token


def telegram_bot(token):
    bot = telebot.TeleBot(token)


# Выводит приветственное сообщение
    @bot.message_handler(commands=['start', 'help'])
    def start_message(message):
        bot.send_message(message.chat.id, "Добро пожаловать в PartyPart\n\n"
                                          "Получить подробную справку о работе бота /info\n"
                                          "Добавить нового участника /add_user\n"
                                          "Добавить траты – Имя юзера Сумма\n"
                                          "Посмотреть траты участника – Имя юзера\n"
                                          "Удалить запись о расходах /del\n"
                                          "Посмотреть итоги /total\n"
                                          "Вызвать справку /help или /start\n"
                                          "Удалить все записи о мероприятии /drop")

# Выводит справку о предназначении бота
    @bot.message_handler(commands=['info'])
    def info_message(message):
        bot.send_message(message.chat.id, "PatryPart – бот для учета расходов на мероприятие.\n\n"
                                          "Предположим, вы с друзьями решили устроить вечеринку:\n"
                                          "– Андрей купил вино за 1050 рублей и мандарины за 240\n"
                                          "– Пётр купил сыр за 500 и виноград за 370\n"
                                          "– Анна заказала суши за 1450\n"
                                          "– Вероника выбрала пиццу за 560\n"
                                          "– Сергей опаздывал на мероприятие и не успел купить ничего\n"
                                          "Вы вносите все эти траты в бота и он рассчитывает кому надо докинуть денег, а кому забрать из общего банка.")

# Добавляет нового участника мероприятия
    @bot.message_handler(commands=['add_user'])
    def add_user(message):
        partypart.add_user(message.chat.id)



    bot.polling()


if __name__ == '__main__':
    # get_data()
    telegram_bot(token)