'''
import requests
import telebot
import logging
from geopy.geocoders import Nominatim
from telebot import types

API_URL = "http://45.8.249.62:5000"

#logging.basicConfig(
 #   format='%(asctime)s -%(name)s -%(message)s',
  #  level=logging.INFO
#)

coord = "0"
name = "0"
floor = "0"
equipment = "0"
time = "0"


# для примера работы кнопки "Информация"
bd = (f"55.7522200, 37.6155600/Жилой дом/4/Дрель/5\n"
      f"45.7234200, 67.6353250/Жилой дом/6/Дрель/2 \n"
      f"45.7234200, 67.6353250/Жилой дом/6/Дрель/2 \n"
      f""f"45.7234200, 67.6353250/Жилой дом/6/Дрель/2 \n")


bot = telebot.TeleBot("5992085801:AAG54zao1cFSm8ZDP13sH75h5IkceDzFJJY")
def get_employees():
    """Get a list of all employees"""
    response = requests.get(f"{API_URL}/employees")
    if response.status_code == 200:
        employees = response.json()
        message_body = 'EMPLOYEES:\n'
        for employee in employees:
            message_body += f"{employee['name']}, {employee['position']}\n"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message_body)
    else:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='Sorry, something went wrong. Please try again later.')

def add_employee(name, position):
    """Add a new employee"""
    response = requests.post(f"{API_URL}/employees", json={'name': name, 'position': position})
    if response.status_code == 201:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='Employee added successfully.')
	else:
		bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='Sorry, something went wrong. Please try again later.')

def update_employee(id, name=None, position=None):
"""Update an existing employee"""
	url = f"{API_URL}/employees/{id}"
	data = {}
	if name:
		data['name'] = name
	if position:
		data['position'] = position
	response = requests.put(url, json=data)
	if response.status_code == 200:
		bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='Employee updated successfully.')
	else:
		bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='Sorry, something went wrong. Please try again later.')

def delete_employee(id):
	"""Delete an employee"""
	url = f"{API_URL}/employees/{id}"
	response = requests.delete(url)
	if response.status_code == 200:
	bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='Employee deleted successfully.')
	else:
	bot.send_message(chat_id=TELEGRAM_CHAT_ID, text='Sorry, something went wrong. Please try again later.')


def get_location(lat, lng):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(str(lat) + "," + str(lng))
    return location.address

@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_time = types.KeyboardButton("Добавить рабочее время")
    item_inf = types.KeyboardButton("Информация")
    bot.send_message(message.chat.id, "Добрый день! Желаете добавить рабочее время?", reply_markup=markup.add(item_time, item_inf))

# добавляем время
@bot.message_handler(commands=["addtime"])
def addtime(message):
    markup2 = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text="Да", callback_data=f"yes")
    item_no = types.InlineKeyboardButton(text="Нет", callback_data="no")
    mass = message.text[9:]
    coord, name, floor, equipment, time = mass.split("/")
    # проверяем есть ли в базе данных такие показатели
    #if coord =
        #if name =
            #if floor =
                #if equipment =
                    #stime = +time (добавляем к имеющемуся времени)
    #elif если нет, то создаем новую строку
    bot.send_message(message.chat.id, f"Вы желаете добавить {time}ч. ?", reply_markup=markup2.add(item_yes, item_no))
    # заполняем запрос в переменную

@bot.callback_query_handler(func= lambda call: True)
def answer(call):
    if call.data == "yes":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Время добавлено")
        # отправляем запрос
    elif call.data == "no":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Время сброшено. Введите данные с помощью команды /addtime")
        # Удаляем запрос из переменной

# обработка сообщений
@bot.message_handler()
def markup(message):
    if message.text == 'Добавить рабочее время':
        bot.send_message(message.chat.id, f"Введите данные о процессе c помощью команды /addtime в виде: \n"
                                          f"/addtime 55.7522200, 37.6155600/Жилой дом/4/Дрель/5 \n"
                                          f"\n"
                                          f"55.7522200, 37.6155600 - коодинаты объекта \n"
                                          f"Жилой дом - название объекта \n"
                                          f"4 - этаж \n"
                                          f"Дрель - название оборудования \n"
                                          f"5 - количество часов \n", reply_markup=types.ReplyKeyboardRemove())
    if message.text.startswith('Информация'):
        bot.send_message(message.chat.id, f"Информация об объектах: \n{bd}", reply_markup=types.ReplyKeyboardRemove())

bot.polling(non_stop=True)
'''
