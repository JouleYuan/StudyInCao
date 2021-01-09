from flask import send_file
from flask_restful import Resource
from models.resource import ResourceModel


class ResourceFile(Resource):
    def get(self, id):
        resource = ResourceModel.query.get(id)
        print(resource.file)
        return send_file('file/resource/' + str(id) + '.' + resource.file, as_attachment=True)


"""class HomeworkFile(Resource):
    def get(self, homework_id, student_id):

        return send_file('file/resource/' + str(homework_id) + '/' + str(student_id) + '.jpeg', as_attachment=True)"""
