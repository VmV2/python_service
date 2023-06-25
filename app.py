from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
import requests
import telebot
import logging
from geopy.geocoders import Nominatim
from telebot import types
API_URL = "http://127.0.0.1:5000"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
bot = telebot.TeleBot('6137135992:AAEVNVGleKNCSXR0ursu3SrWzdlpV49xRWY')


db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    name_of_building = db.Column(db.String(50))
    coordinates = db.Column(db.String(50))
    floors = db.Column(db.Integer)
    equipment = db.Column(db.String(50))
    floor = db.Column(db.Integer)
    hours = db.Column(db.Float)
    def __init__(self, user_id, name_of_building, coordinates, floors, equipment, floor, hours):
        self.user_id = user_id
        self.name_of_building = name_of_building
        self.coordinates = coordinates
        self.floors = floors
        self.equipment = equipment
        self.floor = floor
        self.hours = hours


with app.app_context():   # add existing db check or use alembic
    db.create_all()

@app.route('/add_employee', methods=['POST'])
def add_employee():
    user_id = request.form['user_id']
    name_of_building = request.form['name_of_building']
    coordinates = request.form['coordinates']
    floors = request.form['floors']
    equipment = request.form['equipment']
    floor = request.form['floor']
    hours = request.form['hours']
    employee = Employee(user_id, name_of_building, coordinates, floors, equipment, floor, hours)
    db.session.add(employee)
    db.session.commit()
    return {"success": 'Employee added successfully'}

@app.route('/get_employee/<int:id>')
def get_employee(id):
    employee = Employee.query.get(id)
    if employee:
        return jsonify({
            'id': employee.id,
            'user_id': employee.user_id,
            'name_of_building': employee.name_of_building,
            'coordinates': employee.coordinates,
            'floors': employee.floors,
            'equipment': employee.equipment,
            'floor': employee.floor,
            'hours': employee.hours,
        })
    else:
        return {'error': 'Employee not found'}
@app.route('/delete_employee/int:id', methods=['DELETE'])
def delete_employee(id):
    try:
        employee = Employee.query.get(id)
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'message': 'Employee deleted successfully'})
    except SQLAlchemyError as e:
        error = str(e.dict.get('orig', e))
        return jsonify({'error': error}), 500

@app.route('/update_employee/int:id', methods=['PUT'])
def update_employee(id):
    try:
        employee = Employee.query.get(id)
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        user_id = request.json.get('user_id', employee.user_id)
        name_of_building = request.json.get('name_of_building', employee.name_of_building)
        coordinates = request.json.get('coordinates', employee.coordinates)
        floors = request.json.get('floors', employee.floors)
        equipment = request.json.get('equipment', employee.equipment)
        floor = request.json.get('floor', employee.floor)
        hours = request.json.get('hours', employee.hours)

        employee.user_id = user_id
        employee.name_of_building = name_of_building
        employee.coordinates = coordinates
        employee.floors = floors
        employee.equipment = equipment
        employee.floor = floor
        employee.hours = hours
        db.session.commit()
        return jsonify({'message': 'Employee updated successfully'})
    except SQLAlchemyError as e:
        error = str(e.dict.get('orig', e))
        return jsonify({'error': error}), 500
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup()
    butAd = types.KeyboardButton('Добавить рабочее время')
    butGetInf = types.KeyboardButton('Получить информацию')
    markup.row(butAd, butGetInf)
    bot.send_message(message.chat.id, text='Добро пожаловать. Для добавления рабочего времени необходимого на процесс нажмите на кнопку "Добавить"'.format(message.from_user), reply_markup=markup)
@bot.message_handler(func=lambda message: message.text=="Добавить рабочее время")
def get_text_messages(message):
    global user_id
    user_id = message.from_user.id
    bot.send_message(message.chat.id, 'Введите название здания')
    @bot.message_handler(content_types=['text'])
    def get_name_of_building(message):
        global name_of_building
        name_of_building = message.text
        bot.send_message(message.chat.id, 'Введите адрес здания')
        bot.register_next_step_handler(message, get_coordinates)
    def get_coordinates(message):
        global coordinates
        coordinates = message.text
        bot.send_message(message.chat.id, 'Введите количество этажей в здании')
        bot.register_next_step_handler(message, get_floors)
    def get_floors(message):
        global floors
        floors = message.text
        bot.send_message(message.chat.id, 'Введите название оборудования')
        bot.register_next_step_handler(message, get_equipment)
    def get_equipment(message):
        global equipment
        equipment = message.text
        bot.send_message(message.chat.id, 'Введите этаж, на котором оно размещено')
        bot.register_next_step_handler(message, get_floor)
    def get_floor(message):
        global floor
        floor = message.text
        bot.send_message(message.chat.id, 'Введите количество часов, в течении которых оно будет использоваться')
        bot.register_next_step_handler(message, get_hours)
    def get_hours(message):
        global hours
        hours = message.text
        try:
            res = requests.post(url = "http://127.0.0.1:5000/add_employee", data = {'user_id':user_id,'name_of_building':name_of_building,'coordinates':coordinates, 'floors':floors,'equipment': equipment,'floor':floor,'hours':hours})
        except: bot.send_message('Что-то не отправилось')

bot.polling(non_stop=True)
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)