from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)