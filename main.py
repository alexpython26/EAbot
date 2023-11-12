import telebot
import psycopg2
from telebot import types
from config import *

# Подключаемся к боту
bot = telebot.TeleBot(token)

try:
    # Подключаемся к PostgreSQL

    # connection = psycopg2.connect(
    #     host=host,
    #     user=user,
    #     password=password,
    #     database=db_name
    # )
    #
    # connection.autocommit = True

    class Employee:
        def __init__(self, pin, phone, fullname):
            self.pin = pin
            self.phone = phone
            self.fullname = fullname

        def __str__(self):
            return f'{self.pin}, {self.phone}, {self.fullname}'


    e = Employee('ваш пин без ковычек', 'ваш номер', 'Имя')
    lst = str(e).split(',')


    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """
    #         CREATE TABLE users(
    #         pin varchar(14) PRIMARY KEY,
    #         phone_number varchar(20) NOT NULL,
    #         fullname varchar(50) NOT NULL
    #         )
    #         """
    #     )
    #
    # with connection.cursor() as cursor:
    #     cursor.execute(
    #         """
    #         INSERT INTO users(pin, phone_number, fullname) VALUES ('пин без кавычек', 'номер', 'имя')
    #         """
    #     )

    # cursor = connection.cursor()

    # Обрабатываем стартовое сообщение
    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton('Регистрация')

        markup.add(item)

        bot.send_message(message.chat.id, 'Нажмите кнопку регистрации'.format(message.from_user),
                         reply_markup=markup)


    # Обрабатываем ПИН
    @bot.message_handler(content_types=['text'])
    def pin(message):
        if message.text == 'Регистрация':
            try:
                return bot.reply_to(
                    message, 'Напишите свой ПИН',
                )
            except Exception as err:
                return bot.reply_to(
                    message, err,
                )

        try:
            int(message.text)
        except Exception as err:
            return bot.reply_to(
                message, 'ПИН должен состоять из цифр!',
            )

        if len(message.text) != 14:
            try:
                return bot.reply_to(
                    message, "Длинна ПИНа должна быть 14 символов!",
                )
            except Exception as err:
                return bot.reply_to(
                    message, "Error in code"
                             f'{message.from_user.first_name}',
                )

        # Запрашиваем ПИН с базы данных
        # cursor.execute(
        #     """
        #     SELECT pin FROM users;
        #     """
        # )

        # Сверяем ПИН
        for i in lst:
            if message.text == i:
                try:
                    global pin
                    pin = message.text
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item = types.KeyboardButton('Отправить номер телефона', request_contact=True)
                    markup.add(item)
                    bot.send_message(message.chat.id, 'ПИН подходит, отправьте ваш номер телефона!'.format(
                        message.from_user), reply_markup=markup)
                except Exception as err:
                    return bot.reply_to(
                        message, str(err)
                    )
                break
        else:
            return bot.reply_to(
                message, "ПИН не подходит!",
            )


    # Обрабатываем номер
    @bot.message_handler(content_types=['contact'])
    def phone(message):
        # Приводим номер к общему виду
        if message.contact:
            if message.contact.phone_number.startswith('0'):
                phone_number = 'код страны' + message.contact.phone_number[1:]
            elif message.contact.phone_number.startswith('9'):
                phone_number = '+' + message.contact.phone_number
            # print(message.contact.phone_number)
            # print(phone_number)
            try:
                # Запрашиваем номер с базы данных
                # cursor.execute(
                #     f"""SELECT phone_number FROM users WHERE pin='{pin}';"""
                # )
                # Сверяем номер
                # print(lst)
                for i in lst:
                    # print(i)
                    # print(phone_number == i)
                    if phone_number == i.lstrip():
                        # cursor.execute(
                        #     f"""SELECT fullname FROM users WHERE pin='{pin}';"""
                        # )
                        return bot.reply_to(
                            message, f'Вы зарегистрировались!\nЗдравствуйте, {lst[2]}!'
                        )
                else:
                    return bot.reply_to(
                        message, 'Номер телефона не подходит!'
                    )
            except Exception as err:
                print(err)


except Exception as err:
    print(f'Ошибка подключения к PostgreSql [{err}]')

bot.polling(none_stop=True)

