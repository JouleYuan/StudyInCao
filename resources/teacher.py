from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.teacher import TeacherModel
from common import code, pretty_result
from common.auth import verify_admin_token, verify_id_token


class AllTeachers(Resource):
    def get(self):
        try:
            teachers = TeacherModel.query.all()
            data = [
                {
                    'id': teacher.id,
                    'name': teacher.name,
                    'gender': teacher.gender,
                    'school': teacher.school,
                    'title': teacher.title,
                    'address': teacher.address,
                    'phone': teacher.phone,
                    'email': teacher.email,
                    'description': teacher.description
                    # 'avatar': teacher.avatar
                }
                for teacher in teachers
            ]
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class Teacher(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, id):
        try:
            teacher = TeacherModel.query.get(id)
            data = {
                'id': teacher.id,
                'name': teacher.name,
                'gender': teacher.gender,
                'school': teacher.school,
                'title': teacher.title,
                'address': teacher.address,
                'phone': teacher.phone,
                'email': teacher.email,
                'description': teacher.description
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
        self.parser.add_argument('school', type=str, location="args")
        self.parser.add_argument('title', type=str, location="args")
        args = self.parser.parse_args()

        try:
            teacher = TeacherModel(
                id=id,
                name=args['name'],
                gender=bool(args['gender']),
                school=args['school'],
                title=args['title']
            )
            db.session.add(teacher)
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
        self.parser.add_argument('school', type=str, location="args")
        self.parser.add_argument('title', type=str, location="args")
        args = self.parser.parse_args()

        try:
            teacher = TeacherModel.query.get(id)
            teacher.name = args['name']
            teacher.gender = bool(args['gender'])
            teacher.school = args['school']
            teacher.title = args['title']
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
            teacher = TeacherModel.query.get(id)
            db.session.delete(teacher)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class TeacherDetail(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def put(self, id):
        if verify_id_token(self.token_parser, id) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        self.parser.add_argument('address', type=str, location="args")
        self.parser.add_argument('phone', type=str, location="args")
        self.parser.add_argument('email', type=str, location="args")
        self.parser.add_argument('description', type=str, location="args")
        """self.parser.add_argument('avatar', type=int, location="args")"""
        args = self.parser.parse_args()

        try:
            teacher = TeacherModel.query.get(id)
            teacher.address = args['address']
            teacher.phone = args['phone']
            teacher.email = args['email']
            teacher.description = args['description']
            """teacher.avatar = """
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
