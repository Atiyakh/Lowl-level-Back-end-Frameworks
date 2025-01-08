from MiddleWare.Database import Models

# FIXME Make AutoField auto!

class Teacher(Models.Model):
    first_name = Models.CharField(max_length=300, primary_key=True)
    last_name = Models.CharField(max_length=300)
    phone_number = Models.IntegerField()
    teacher_image = Models.FilePathField(allow_null=True, unique=True)

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
