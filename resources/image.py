from flask import send_file
from flask_restful import Resource


class Image(Resource):
    def get(self, type, id):
        return send_file('file/avatar/' + type + '/' + str(id) + '.jpeg', mimetype='image/jpeg')
