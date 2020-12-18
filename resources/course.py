from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.course import CourseModel
from models.user import UserModel
from common import code, pretty_result
from common.auth import verify_admin_token, verify_id_token


class AllCourses(Resource):
    def get(self):
        try:
            courses = CourseModel.query.all()
            data = [
                {
                    'id': course.id,
                    'name': course.name,
                    'teacher_id': course.teacher_id,
                    'assistant_id': course.assistant_id,
                    'time': course.time,
                    'address': course.address,
                    'description': course.description
                }
                for course in courses
            ]
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class PostCourse(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def post(self):
        if verify_admin_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        self.parser.add_argument('name', type=str, location="args")
        self.parser.add_argument('teacher_id', type=str, location="args")
        self.parser.add_argument('time', type=str, location="args")
        self.parser.add_argument('address', type=str, location="args")
        args = self.parser.parse_args()

        try:
            user = CourseModel(
                name=args['name'],
                teacher_id=args['teacher_id'],
                time=args['time'],
                address=args['address'],
            )
            db.session.add(user)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class Course(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, id):
        try:
            course = CourseModel.query.get(id)
            data = {
                'name': course.name,
                'teacher_id': course.teacher_id,
                'assistant_id': course.assistant_id,
                'time': course.time,
                'address': course.address,
                'description': course.description
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def put(self, id):
        if verify_admin_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        self.parser.add_argument('name', type=str, location="args")
        self.parser.add_argument('teacher_id', type=str, location="args")
        self.parser.add_argument('time', type=str, location="args")
        self.parser.add_argument('address', type=str, location="args")
        args = self.parser.parse_args()

        try:
            course = CourseModel.query.get(id)
            course.name = args['name']
            course.teacher_id = args['teacher_id']
            course.time = args['time']
            course.address = args['address']
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
            course = CourseModel.query.get(id)
            db.session.delete(course)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class CourseDetail(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def put(self, id):
        try:
            course = CourseModel.query.get(id)

            if verify_id_token(self.token_parser, course.teacher_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            self.parser.add_argument('assistant_id', type=str, location="args")
            self.parser.add_argument('description', type=str, location="args")
            args = self.parser.parse_args()

            user = UserModel.query.get(id)
            if not user.is_assistant:
                return pretty_result(code.OTHER_ERROR, 'assistant does not exist')

            course.assistant_id = args['assistant_id']
            course.description = args['description']
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)