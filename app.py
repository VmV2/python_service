from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask import Flask
import httpx
import requests
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    position = db.Column(db.String(50))

    def __init__(self, name, position):
        self.name = name
        self.position = position


db.create_all()


@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = requests.form['name']
    position = requests.form['position']
    employee = Employee(name=name, position=position)
    db.session.add(employee)
    db.session.commit()
    return {"success": 'Employee added successfully'}


@app.route('/get_employee/<int:id>')
def get_employee(id):
    employee = Employee.query.get(id)
    if employee:
        return jsonify({
            'id': employee.id,
            'name': employee.name,
            'position': employee.position
        })
    else:
        return {'error': 'Employee not found'}