from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'

db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    position = db.Column(db.String(50))

    def __init__(self, name, position):
        self.name = name
        self.position = position


with app.app_context():   # add existing db check or use alembic
    db.create_all()

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.form['name']
    position = request.form['position']
    employee = Employee(name, position)
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
