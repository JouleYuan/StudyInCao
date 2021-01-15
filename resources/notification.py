from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.notification import NotificationModel
from models.course import CourseModel
from models.course_student import CourseStudentModel
from common import code, pretty_result
from common.auth import verify_id_token, verify_student_token


class StudentNotification(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, student_id):
        if (verify_student_token(self.token_parser) and verify_id_token(self.token_parser, student_id)) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        try:
            data = []
            notifications = NotificationModel.query.filter_by(student_id=student_id).all()
            for notification in notifications:
                course = CourseModel.query.get(notification.course_id)
                data.append({
                    'id': notification.id,
                    'course_id': notification.course_id,
                    'course_name': course.name,
                    'content_type': notification.content_type,
                    'content_title': notification.content_title,
                    'content': notification.content,
                    'state': notification.state,
                    'time': str(notification.time),
                    'is_read': notification.is_read,
                })
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def put(self, student_id):
        if (verify_student_token(self.token_parser) and verify_id_token(self.token_parser, student_id)) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        try:
            notifications = NotificationModel.query.filter_by(student_id=student_id).all()
            for notification in notifications:
                notification.is_read = 1
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class CourseNotification(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, course_id):
        try:
            course = CourseModel.query.get(course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            notifications = NotificationModel.query.filter_by(course_id=course_id).all()
            data = [{
                'id': notification.id,
                'course_id': notification.course_id,
                'course_name': course.name,
                'content_type': notification.content_type,
                'content_title': notification.content_title,
                'content': notification.content,
                'state': notification.state,
                'time': str(notification.time),
                'is_read': notification.is_read,
            } for notification in notifications]
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def post(self, course_id):
        try:
            course = CourseModel.query.get(course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            self.parser.add_argument('title', type=str, location="args")
            self.parser.add_argument('content', type=str, location="form")
            args = self.parser.parse_args()

            students = CourseStudentModel.query.filter_by(course_id=course.id).all()
            for student in students:
                notification = NotificationModel(
                    student_id=student.student_id,
                    course_id=course_id,
                    content_type="发布",
                    content_title=args['title'],
                    content=args['content'],
                    state=1,
                )
                db.session.add(notification)

            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
