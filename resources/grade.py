from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.course import CourseModel
from models.course_student import CourseStudentModel
from models.student import StudentModel
from common import code, pretty_result
from common.auth import verify_admin_token, verify_id_token


class CourseStudentGrade(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, course_id, student_id):
        try:
            course = CourseModel.query.get(course_id)
            if verify_id_token(self.token_parser, student_id) is False \
                    and verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False \
                    and verify_admin_token(self.token_parser) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            course_student = CourseStudentModel.query.filter_by(course_id=course_id, student_id=student_id).first()
            data = {'grade': course_student.grade}
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def put(self, course_id, student_id):
        try:
            course = CourseModel.query.get(course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False and\
                    verify_admin_token(self.token_parser) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            self.parser.add_argument('grade', type=int, location="args")
            args = self.parser.parse_args()

            course_student = CourseStudentModel.query.filter_by(course_id=course_id, student_id=student_id).first()
            course_student.grade = args['grade']
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class CourseGrade(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, course_id):
        try:
            course = CourseModel.query.get(course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False \
                    and verify_admin_token(self.token_parser) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            data = []
            course_students = CourseStudentModel.query.filter_by(course_id=course_id).all()
            for course_student in course_students:
                student = StudentModel.query.get(course_student.student_id)
                data.append({
                    'id': student.id,
                    'name': student.name,
                    'gender': student.gender,
                    'class_name': student.class_name,
                    'grade': course_student.grade
                })

            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class StudentGrade(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, student_id):
        if verify_id_token(self.token_parser, student_id) is False \
                and verify_admin_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        try:
            course_students = CourseStudentModel.query.filter_by(student_id=student_id).all()
            data = [{
                'course_id': course_student.course_id,
                'grade': course_student.grade
            } for course_student in course_students]
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
