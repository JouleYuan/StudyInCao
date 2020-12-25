from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.student import StudentModel
from common import code, pretty_result, file
from common.auth import verify_admin_token, verify_id_token
from werkzeug.datastructures import FileStorage


class AllStudents(Resource):
    def get(self):
        try:
            students = StudentModel.query.all()
            data = []
            for student in students:
                avatar = None
                if student.avatar is not None:
                    avatar = 'image/student/' + str(student.id)
                data.append({
                    'id': student.id,
                    'name': student.name,
                    'gender': student.gender,
                    'class_name': student.class_name,
                    'email': student.email,
                    'avatar': avatar
                })
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class Student(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, id):
        try:
            student = StudentModel.query.get(id)
            avatar = None
            if student.avatar is not None:
                avatar = 'image/student/' + str(student.id)
            data = {
                'name': student.name,
                'gender': student.gender,
                'class_name': student.class_name,
                'email': student.email,
                'avatar': avatar
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def post(self, id):
        if verify_admin_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        self.parser.add_argument('name', type=str, location="args")
        self.parser.add_argument('gender', type=int, location="args")
        self.parser.add_argument('class_name', type=str, location="args")
        args = self.parser.parse_args()

        try:
            student = StudentModel(
                id=id,
                name=args['name'],
                gender=bool(args['gender']),
                class_name=args['class_name']
            )
            db.session.add(student)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def put(self, id):
        if verify_admin_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        self.parser.add_argument('name', type=str, location="args")
        self.parser.add_argument('gender', type=int, location="args")
        self.parser.add_argument('class_name', type=str, location="args")
        args = self.parser.parse_args()

        try:
            student = StudentModel.query.get(id)
            student.name = args['name']
            student.gender = bool(args['gender'])
            student.class_name = args['class_name']
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def delete(self, id):
        if verify_admin_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        try:
            student = StudentModel.query.get(id)
            file.delete_avatar(student, 'student')
            db.session.delete(student)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class StudentDetail(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def put(self, id):
        if verify_id_token(self.token_parser, id) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        self.parser.add_argument('email', type=str, location="args")
        self.parser.add_argument('avatar', type=FileStorage, location="files")
        args = self.parser.parse_args()

        try:
            student = StudentModel.query.get(id)
            if args['email'] is not None:
                student.email = args['email']
            file.upload_avatar(args['avatar'], student, 'student')
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
