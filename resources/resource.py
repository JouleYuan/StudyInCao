from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.course import CourseModel
from models.chapter import ChapterModel
from models.resource import ResourceModel
from models.course_student import CourseStudentModel
from models.notification import NotificationModel
from common import code, pretty_result, file
from common.auth import verify_id_token
from werkzeug.datastructures import FileStorage


class AllResource(Resource):
    def get(self):
        try:
            resources = ResourceModel.query.all()
            data = [
                {
                    'id': resource.id,
                    'chapter_id': resource.chapter_id,
                    'title': resource.title,
                    'content': resource.content,
                    'time': str(resource.time),
                    'file': 'file/resource/' + str(resource.id)
                }
                for resource in resources
            ]
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class CourseResource(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, course_id):
        try:
            data = []
            chapters = ChapterModel.query.filter_by(course_id=course_id).all()
            for chapter in chapters:
                chapter_data = {
                    'chapter_id': chapter.id,
                    'chapter_no': chapter.no,
                    'resources': []
                }
                resources = ResourceModel.query.filter_by(chapter_id=chapter.id).all()
                chapter_data['resources'] = [
                    {
                        'id': resource.id,
                        'title': resource.title,
                        'content': resource.content,
                        'time': str(resource.time),
                        'file': 'file/resource/' + str(resource.id)
                    }
                    for resource in resources
                ]
                data.append(chapter_data)
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class ChapterResource(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, chapter_id):
        try:
            resources = ResourceModel.query.filter_by(chapter_id=chapter_id).all()
            data = [
                {
                    'id': resource.id,
                    'title': resource.title,
                    'content': resource.content,
                    'time': str(resource.time),
                    'file': 'file/resource/' + str(resource.id)
                }
                for resource in resources
            ]
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def post(self, chapter_id):
        try:
            chapter = ChapterModel.query.get(chapter_id)
            course = CourseModel.query.get(chapter.course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            self.parser.add_argument('title', type=str, location="args")
            self.parser.add_argument('content', type=str, location="form")
            self.parser.add_argument('file', type=FileStorage, location="files")
            args = self.parser.parse_args()

            resource = ResourceModel(
                chapter_id=chapter_id,
                title=args['title'],
                content=args['content'],
            )
            db.session.add(resource)

            students = CourseStudentModel.query.filter_by(course_id=course.id).all()
            file.upload_resource(args['file'], resource)
            for student in students:
                notification = NotificationModel(
                    student_id=student.student_id,
                    content_type="资料",
                    content_title=args['title'],
                    state=1,
                )
                db.session.add(notification)

            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class IdResource(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, id):
        try:
            resource = ResourceModel.query.get(id)
            data = {
                'chapter_id': resource.chapter_id,
                'title': resource.title,
                'content': resource.content,
                'time': str(resource.time),
                'file': 'file/resource/' + str(resource.id)
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def put(self, id):
        try:
            resource = ResourceModel.query.get(id)
            chapter = ChapterModel.query.get(resource.chapter_id)
            course = CourseModel.query.get(chapter.course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            self.parser.add_argument('title', type=str, location="args")
            self.parser.add_argument('content', type=str, location="form")
            self.parser.add_argument('file', type=FileStorage, location="files")
            args = self.parser.parse_args()

            if args['title'] is not None:
                resource.title = args['title']
            if args['content'] is not None:
                resource.content = args['content']
            file.upload_resource(args['file'], resource)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def delete(self, id):
        try:
            resource = ResourceModel.query.get(id)
            chapter = ChapterModel.query.get(resource.chapter_id)
            course = CourseModel.query.get(chapter.course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            db.session.delete(resource)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
