from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.user import UserModel
from common import code, hash_md5, pretty_result
from common.auth import create_login_token, create_modify_password_token, verify_login_token


class Login(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        self.parser.add_argument('id', type=str, location="args")
        self.parser.add_argument('password', type=str, location="args")
        self.parser.add_argument('identity', type=str, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel.query.get(args['id'])
            if user is None or user.password != hash_md5(args['password']):
                return pretty_result(code.AUTHORIZATION_ERROR)
            if (args['identity'] == 'student' and user.is_student is True) or \
               (args['identity'] == 'teacher' and user.is_teacher is True) or \
               (args['identity'] == 'assistant' and user.is_assistant is True) or \
               (args['identity'] == 'admin' and user.is_admin is True):
                token = str(create_login_token({
                    'status': 'login',
                    'id': user.id,
                    'identity': args['identity']
                }), encoding='utf-8')
                return pretty_result(code.OK, data=token)
            else:
                return pretty_result(code.AUTHORIZATION_ERROR)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class ForgotPassword(Resource):
    def __init__(self):
        self.parser = RequestParser()

    def get(self):
        self.parser.add_argument('id', type=str, location="args")
        self.parser.add_argument('answer', type=str, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel.query.get(args['id'])
            if user is not None and user.answer == hash_md5(args['answer']):
                token = str(create_modify_password_token({
                    'status': 'modify_password',
                    'id': user.id
                }), encoding='utf-8')
                return pretty_result(code.OK, data=token)
            else:
                return pretty_result(code.AUTHORIZATION_ERROR)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class ResetPassword(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self):
        if verify_login_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        self.parser.add_argument('id', type=str, location="args")
        self.parser.add_argument('password', type=str, location="args")
        args = self.parser.parse_args()

        try:
            user = UserModel.query.get(args['id'])
            if user is not None and user.password == hash_md5(args['password']):
                token = str(create_modify_password_token({
                    'status': 'modify_password',
                    'id': user.id
                }), encoding='utf-8')
                return pretty_result(code.OK, data=token)
            else:
                return pretty_result(code.AUTHORIZATION_ERROR)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
