from flask import send_file
from flask_restful import Resource
from models.resource import ResourceModel
from models.homework_student import HomeworkStudentModel


class ResourceFile(Resource):
    def get(self, id):
        resource = ResourceModel.query.get(id)
        return send_file('file/resource/' + str(id) + '.' + resource.file, as_attachment=True)


class HomeworkFile(Resource):
    def get(self, id):
        homework_student = HomeworkStudentModel.query.get(id)
        return send_file('file/homework/' + str(id) + '.' + homework_student.file, as_attachment=True)
