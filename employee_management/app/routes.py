from flask import Blueprint, request, jsonify
from . import db
from .models import Employee
from .schemas import employee_schema, employees_schema
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from .error import not_found_error, bad_request_error, internal_error

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return "WELCOME TO THE EMPLOYEE MANAGEMENT SYSTEM"

@routes.route('/employee', methods=['POST'])
def create_employee():
    if request.content_type != 'application/json':
        return bad_request_error("Content-Type must be application/json")

    try:
        data = request.get_json()
        new_emp = employee_schema.load(data)
        employee = Employee(
            name=new_emp['name'], 
            department=new_emp['department'], 
            age=new_emp['age'], 
            position=new_emp['position'], 
            salary=new_emp['salary']
        )

        db.session.add(employee)
        db.session.commit()
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except SQLAlchemyError as e:
        return internal_error(e)

    return jsonify(employee_schema.dump(employee)), 201

@routes.route('/employee/<int:employee_id>', methods=['GET'])
def get_emp(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return not_found_error("Employee not found")

    return jsonify(employee_schema.dump(employee)), 200

@routes.route('/employee/<int:employee_id>', methods=['PUT'])
def update_emp(employee_id):
    if request.content_type != 'application/json':
        return bad_request_error("Content-Type must be application/json")

    employee = Employee.query.get(employee_id)
    if not employee:
        return not_found_error("Employee not found")

    try:
        data = request.get_json()
        updated_data = employee_schema.load(data, partial=True)

        if 'name' in updated_data:
            employee.name = updated_data['name']
        if 'department' in updated_data:
            employee.department = updated_data['department']
        if 'age' in updated_data:
            employee.age = updated_data['age']
        if 'position' in updated_data:
            employee.position = updated_data['position']
        if 'salary' in updated_data:
            employee.salary = updated_data['salary']

        db.session.commit()
    except ValidationError as e:
        return jsonify({"errors": e.messages}), 400
    except SQLAlchemyError as e:
        return internal_error(e)

    return jsonify({"message": "Employee updated successfully"}), 200

@routes.route('/employee/<int:employee_id>', methods=['DELETE'])
def delete_emp(employee_id):
    employee = Employee.query.get(employee_id)
    if not employee:
        return not_found_error("Employee not found")

    try:
        db.session.delete(employee)
        db.session.commit()
    except SQLAlchemyError as e:
        return internal_error(e)

    return jsonify({"message": "Employee deleted successfully!"}), 200
