from importlib.machinery import SourceFileLoader
import os, pathlib
Models = SourceFileLoader("Models", os.path.join(pathlib.Path(__file__).parent, 'MiddleWare/Database/Models.py')).load_module()

class Teacher(Models.Model):
    first_name = Models.CharField(max_length=300, primary_key=True)
    last_name = Models.CharField(max_length=300)
    phone_number = Models.IntegerField()

class Student(Models.Model):
    first_name = Models.CharField(max_length=300)
    last_name = Models.CharField(max_length=300)
    phone_number = Models.IntegerField()
    teacher_firstname = Models.ForeignKey(Teacher.first_name, on_delete=Models.CASCADE)
    teacher_lastname = Models.ForeignKey(Teacher.last_name, on_delete=Models.CASCADE)

class Classroom(Models.Model):
    first_name = Models.CharField(max_length=300)
    last_name = Models.CharField(max_length=300)
    phone_number = Models.IntegerField()
    teacher_firstname = Models.ForeignKey(Teacher.first_name, on_delete=Models.CASCADE)
    teacher_lastname = Models.ForeignKey(Teacher.last_name, on_delete=Models.CASCADE)
