from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.user import UserModel
from common import code, hash_md5, pretty_result
from common.auth import verify_admin_token, verify_id_token, verify_modify_password_token


class AllUsers(Resource):
    """def __init__(self):
        self.token_parser = RequestParser()"""

    def get(self):
        """if verify_admin_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)"""

        try:
            users = UserModel.query.all()
            data = [
                {
                    'id': user.id,
                    'is_student': user.is_student,
                    'is_teacher': user.is_teacher,
                    'is_assistant': user.is_assistant,
                    'is_admin': user.is_admin
                }
                for user in users
            ]
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class User(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, id):
        try:
            user = UserModel.query.get(id)
            data = {
                'is_student': user.is_student,
                'is_teacher': user.is_teacher,
                'is_assistant': user.is_assistant,
                'is_admin': user.is_admin,
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def post(self, id):
        if verify_admin_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        self.parser.add_argument('card_id', type=str, location="args")
        self.parser.add_argument('is_student', type=int, location="args")
        self.parser.add_argument('is_teacher', type=int, location="args")
        self.parser.add_argument('is_assistant', type=int, location="args")
        self.parser.add_argument('is_admin', type=int, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel(
                id=id,
                question='你的身份证号码是多少？',
                password=hash_md5(args['card_id'][-6:]),
                answer=hash_md5(args['card_id']),
                is_student=bool(args['is_student']),
                is_teacher=bool(args['is_teacher']),
                is_assistant=bool(args['is_assistant']),
                is_admin=bool(args['is_admin'])
            )
            db.session.add(user)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def put(self, id):
        if verify_admin_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        self.parser.add_argument('is_student', type=int, location="args")
        self.parser.add_argument('is_teacher', type=int, location="args")
        self.parser.add_argument('is_assistant', type=int, location="args")
        self.parser.add_argument('is_admin', type=int, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel.query.get(id)
            user.is_student = bool(args['is_student'])
            user.is_teacher = bool(args['is_teacher'])
            user.is_assistant = bool(args['is_assistant'])
            user.is_admin = bool(args['is_admin'])
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
            user = UserModel.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class Password(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def put(self, id):
        if verify_modify_password_token(self.token_parser, id) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        self.parser.add_argument('password', type=str, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel.query.get(id)
            user.password = hash_md5(args['password'])
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class Question(Resource):
    def __init__(self):
        self.token_parser = RequestParser()

    def get(self, id):
        if verify_id_token(self.token_parser, id) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        try:
            user = UserModel.query.get(id)
            data = {'question': user.question}
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
