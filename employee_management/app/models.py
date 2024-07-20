# app/models.py

from . import db

#from flask_sqlalchemy import SQLALchemy

 

#db=SQLALchemy(app)

class Employee(db.Model):

 

    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    department = db.Column(db.String(100), nullable=False)

    age = db.Column(db.Integer,nullable=False)

    def _init_(self,name,department,age):

        self.name=name

        self.department=department

        self.age=age

    def to_dict(self):

        return {

               "id":self.id,

            "name":self.name,

            "department":self.department,

            "age":self.age

            }

    def _repr_(self):

        return f'<Employee {self.name}>'


