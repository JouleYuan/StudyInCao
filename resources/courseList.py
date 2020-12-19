from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.course import CourseModel
from models.course_student import CourseStudentModel
from models.teacher import TeacherModel
from common import code, pretty_result
from common.auth import verify_id_token, verify_student_token, verify_teacher_token


class StudentCourseList(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, student_id):
        if (verify_id_token(self.token_parser, student_id) and verify_student_token(self.token_parser)) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        try:
            data = []
            course_students = CourseStudentModel.query.filter_by(student_id=student_id).all()
            for c in course_students:
                course = CourseModel.query.get(c.course_id)
                teacher = TeacherModel.query.get(course.teacher_id)
                time = course.time.split(';')
                for t in time:
                    data.append({
                        'id': course.id,
                        'name': course.name,
                        'teacher': teacher.name,
                        'no': list(map(int, t.split(',')[1:])),
                        'date': int(t.split(',')[0]),
                        'address': course.address
                    })
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class TeacherCourseList(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, teacher_id):
        if (verify_id_token(self.token_parser, teacher_id) and verify_teacher_token(self.token_parser)) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        try:
            data = []
            courses = CourseModel.query.filter_by(teacher_id=teacher_id).all()
            for course in courses:
                time = course.time.split(';')
                for t in time:
                    data.append({
                        'id': course.id,
                        'name': course.name,
                        'no': list(map(int, t.split(',')[1:])),
                        'date': int(t.split(',')[0]),
                        'address': course.address
                    })
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
