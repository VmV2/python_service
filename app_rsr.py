from flask_restful import Resource, Api
from flask import Flask, jsonify
app = Flask(__name__)
api = Api(app)


class Employee(Resource):
    def get(self):
        return jsonify({'employee': 'John Doe'})

api.add_resource(Employee, '/employees')

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)