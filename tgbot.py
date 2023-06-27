import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot("5992085801:AAG54zao1cFSm8ZDP13sH75h5IkceDzFJJY")

number_str = 0
conn = sqlite3.connect("bot.db")
cursor = conn.execute('SELECT * FROM users')
for raw in cursor:
    number_str = number_str + 1

conn.close()

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    butAd = types.KeyboardButton('Добавить рабочее время')
    butGetInf = types.KeyboardButton('Информация')
    markup.row(butAd, butGetInf)
    bot.send_message(message.chat.id, text='Добро пожаловать! \nЧтобы добавить рабочее время нажмите на кнопку "Добавить рабочее время"(/addtime)\n'
                                           'Чтобы получить информацию об объектах нажмине на кнопку "Информация"(/info)\n'
                                           'Чтобы удалить информацию об объеке воспользуйтесь командой '
                                           '/del *, где * - номер строки'.format(message.from_user), reply_markup=markup)

@bot.message_handler(func=lambda message: message.text=="Добавить рабочее время" or message.text== "/addtime")
def get_text_messages(message):
    global user_id
    user_id = int(message.from_user.id)
    bot.send_message(message.chat.id, 'Введите название здания:', reply_markup=types.ReplyKeyboardRemove())
    @bot.message_handler(content_types=['text'])
    def get_name_of_building(message):
        global name_of_building
        name_of_building = str(message.text)
        bot.send_message(message.chat.id, 'Введите адрес здания:')
        bot.register_next_step_handler(message, get_coordinates)
    def get_coordinates(message):
        global coordinates
        coordinates = str(message.text)
        bot.send_message(message.chat.id, 'Введите количество этажей в здании:')
        bot.register_next_step_handler(message, get_floors)
    def get_floors(message):
        global floors
        try:
            floors = int(message.text)
            bot.send_message(message.chat.id, 'Введите название оборудования:')
            bot.register_next_step_handler(message, get_equipment)
        except ValueError:
            bot.send_message(message.chat.id, 'Некорректное значение! Введите количество этажей в здании:')
            bot.register_next_step_handler(message, get_floors)
    def get_equipment(message):
        global equipment
        equipment = str(message.text)
        bot.send_message(message.chat.id, 'Введите этаж, на котором оно размещено:')
        bot.register_next_step_handler(message, get_floor)
    def get_floor(message):
        global floor
        try:
            floor = int(message.text)
            bot.send_message(message.chat.id, 'Введите количество часов, в течении которых оно будет использоваться:')
            bot.register_next_step_handler(message, get_hours)
        except ValueError:
            bot.send_message(message.chat.id, 'Некорректное значение! Введите этаж, на котором оно размещено:')
            bot.register_next_step_handler(message, get_floor)
    def get_hours(message):
        global hours
        global number_str
        try:
            hours = float(message.text)
            conn = sqlite3.connect("bot.db")
            cursor = conn.cursor()
            cursor.execute(f"select hours from users where name_of_building = '{name_of_building}' "
                           f"AND coordinates = '{coordinates}' "
                           f"AND equipment = '{equipment}' "
                           f"AND floor = {floor} "
                           f"AND floors = {floors}")
            hours_1 = cursor.fetchone()
            conn.close()
            if hours_1:
                hours_sum = hours_1[0] + hours
                conn = sqlite3.connect("bot.db")
                conn.execute(f"UPDATE users SET hours = {hours_sum} WHERE name_of_building = '{name_of_building}' "
                             f"AND coordinates = '{coordinates}' "
                             f"AND equipment = '{equipment}' "
                             f"AND floor = {floor} "
                             f"AND floors = {floors}")
                conn.commit()
                conn.close()
                bot.send_message(message.chat.id, f'Для объекта "{name_of_building}" добавлено {hours} часов!')
            else:
                try:
                    number_id = number_str + 1
                    conn = sqlite3.connect("bot.db")
                    cursor = conn.cursor()
                    cursor.execute(f"INSERT INTO users (id, user_id, name_of_building, coordinates, equipment, floor, floors, hours) "
                                   f"VALUES ({number_id}, {user_id}, '{name_of_building}', '{coordinates}', '{equipment}', {floor}, {floors}, {hours})")
                    conn.commit()
                    conn.close()
                    bot.send_message(message.chat.id, f"Данные успешно добавлены!")
                    number_str = number_str + 1
                except sqlite3.Error:
                    bot.send_message(message.chat.id, f"Данные введены не корректно!")
        except ValueError:
            bot.send_message(message.chat.id, 'Некорректное значение! Введите количество часов, в течении которых оно будет использоваться:')
            bot.register_next_step_handler(message, get_hours)

@bot.message_handler(commands= ["del"])
def del_str_messages(message):
    global number_str
    del_t = message.text.split()
    if len(del_t) == 2:
        id_str = int(del_t[1])
        conn = sqlite3.connect("bot.db")
        cursor = conn.cursor()
        cursor.execute(f"DELETE from users where id = {id_str}")
        bot.send_message(message.chat.id, f'Строка под номером {id_str} удалена')
        number_str = number_str - 1
        cursor.execute('CREATE TEMP VIEW temp_view AS SELECT *, ROW_NUMBER() OVER () AS row_num FROM users')
        cursor.execute('UPDATE users SET id = (SELECT row_num FROM temp_view WHERE users.id = temp_view.id)')
        conn.commit()
        conn.close()
    else:
        bot.send_message(message.chat.id, 'Введите команду /del в формате: /del *, где * - номер строки')

@bot.message_handler(func=lambda message: message.text=="Информация" or message.text== "/info")
def get_text(message):
    global number_str
    bot.send_message(message.chat.id, f"Найдено записей: {number_str}")
    conn = sqlite3.connect("bot.db")
    cursor = conn.execute('SELECT * FROM users')
    for raw in cursor:
        bot.send_message(message.chat.id, f"|{raw[0]}|{raw[2]}|{raw[3]}|{raw[4]}|{raw[5]}|{raw[6]}|{raw[7]}|",
                         reply_markup=types.ReplyKeyboardRemove())

    conn.close()

bot.polling()
