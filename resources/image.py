from flask import send_file
from flask_restful import Resource
from models.course import CourseModel
from models.student import StudentModel
from models.teacher import TeacherModel


class CourseImage(Resource):
    def get(self, id):
        course = CourseModel.query.get(id)
        return send_file('file/avatar/course/' + str(id) + '.' + course.avatar)


class StudentImage(Resource):
    def get(self, id):
        student = StudentModel.query.get(id)
        return send_file('file/avatar/student/' + id + '.' + student.avatar)


class TeacherImage(Resource):
    def get(self, id):
        teacher = TeacherModel.query.get(id)
        return send_file('file/avatar/teacher/' + id + '.' + teacher.avatar)
