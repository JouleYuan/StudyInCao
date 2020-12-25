from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.course import CourseModel
from models.course_student import CourseStudentModel
from models.user import UserModel
from models.teacher import TeacherModel
from common import code, pretty_result, file
from common.auth import verify_admin_token, verify_id_token
from werkzeug.datastructures import FileStorage


class AllCourses(Resource):
    def get(self):
        try:
            data = []
            courses = CourseModel.query.all()
            for course in courses:
                teacher = TeacherModel.query.get(course.teacher_id)
                avatar = None
                if course.avatar is not None:
                    avatar = 'image/course/' + str(course.id)
                data.append({
                    'id': course.id,
                    'name': course.name,
                    'teacher_id': course.teacher_id,
                    'teacher_name': teacher.name,
                    'assistant_id': course.assistant_id,
                    'time': course.time,
                    'address': course.address,
                    'classification': teacher.school,
                    'general': course.general,
                    'description': course.description,
                    'introduce': course.introduce,
                    'plan': course.plan,
                    'material': course.material,
                    'exam': course.exam,
                    'request': course.request,
                    'avatar': avatar
                })
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
            course = CourseModel(
                name=args['name'],
                teacher_id=args['teacher_id'],
                time=args['time'],
                address=args['address'],
            )
            db.session.add(course)
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
            teacher = TeacherModel.query.get(course.teacher_id)
            avatar = None
            if course.avatar is not None:
                avatar = 'image/course/' + str(course.id)
            data = {
                'id': course.id,
                'name': course.name,
                'teacher_id': course.teacher_id,
                'teacher_name': teacher.name,
                'assistant_id': course.assistant_id,
                'time': course.time,
                'address': course.address,
                'classification': teacher.school,
                'general': course.general,
                'description': course.description,
                'introduce': course.introduce,
                'plan': course.plan,
                'material': course.material,
                'exam': course.exam,
                'request': course.request,
                'avatar': avatar
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

            self.parser.add_argument('assistant_id', type=str, location="form")
            self.parser.add_argument('general', type=str, location="form")
            self.parser.add_argument('description', type=str, location="form")
            self.parser.add_argument('introduce', type=str, location="form")
            self.parser.add_argument('plan', type=str, location="form")
            self.parser.add_argument('material', type=str, location="form")
            self.parser.add_argument('exam', type=str, location="form")
            self.parser.add_argument('request', type=str, location="form")
            self.parser.add_argument('avatar', type=FileStorage, location="files")
            args = self.parser.parse_args()

            if args['assistant_id'] is not None:
                user = UserModel.query.get(args['assistant_id'])
                if not user.is_assistant:
                    return pretty_result(code.OTHER_ERROR, 'assistant does not exist')
                course.assistant_id = args['assistant_id']
            if args['general'] is not None:
                course.general = args['general']
            if args['description'] is not None:
                course.description = args['description']
            if args['introduce'] is not None:
                course.introduce = args['introduce']
            if args['plan'] is not None:
                course.plan = args['plan']
            if args['material'] is not None:
                course.material = args['material']
            if args['exam'] is not None:
                course.exam = args['exam']
            if args['request'] is not None:
                course.request = args['request']
            file.upload_avatar(args['avatar'], course, 'course')
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class CourseStudent(Resource):
    def __init__(self):
        self.token_parser = RequestParser()

    def post(self, course_id, student_id):
        if verify_admin_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        try:
            course_student = CourseStudentModel(
                course_id=course_id,
                student_id=student_id
            )
            db.session.add(course_student)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def delete(self, course_id, student_id):
        if verify_admin_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        try:
            course_student = CourseStudentModel.query.filter_by(course_id=course_id, student_id=student_id).first()
            db.session.delete(course_student)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)