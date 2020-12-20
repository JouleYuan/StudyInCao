# file upload is not finished
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.course import CourseModel
from models.chapter import ChapterModel
from models.resource import ResourceModel
from common import code, pretty_result
from common.auth import verify_id_token


class AllResource(Resource):
    def get(self):
        try:
            resources = ResourceModel.query.all()
            data = [
                {
                    'chapter_id': resource.chapter_id,
                    'no': resource.no,
                    'title': resource.title,
                    'content': resource.content,
                    'file': resource.file
                }
                for resource in resources
            ]
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
                    'no': resource.no,
                    'title': resource.title,
                    'content': resource.content,
                    'file': resource.file
                }
                for resource in resources
            ]
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class ChapterNoResource(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, chapter_id, no):
        try:
            resource = ResourceModel.query.filter_by(chapter_id=chapter_id, no=no).first()
            data = {
                'title': resource.title,
                'content': resource.content,
                'file': resource.file
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def post(self, chapter_id, no):
        try:
            chapter = ChapterModel.query.get(chapter_id)
            course = CourseModel.query.get(chapter.course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            self.parser.add_argument('title', type=str, location="args")
            self.parser.add_argument('content', type=str, location="form")
            args = self.parser.parse_args()

            resource = ResourceModel.query.filter_by(course_id=chapter_id, no=no).first()
            if resource is not None:
                return pretty_result(code.DB_ERROR)

            resource = ResourceModel(
                chapter_id=chapter_id,
                no=no,
                title=args['title'],
                content=args['content'],
                file=''
            )
            db.session.add(resource)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def put(self, chapter_id, no):
        try:
            chapter = ChapterModel.query.get(chapter_id)
            course = CourseModel.query.get(chapter.course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            self.parser.add_argument('title', type=str, location="args")
            self.parser.add_argument('content', type=str, location="form")
            args = self.parser.parse_args()

            resource = ResourceModel.query.filter_by(course_id=chapter_id, no=no).first()
            resource.title = args['title']
            resource.content = args['content']
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def delete(self, chapter_id, no):
        try:
            chapter = ChapterModel.query.get(chapter_id)
            course = CourseModel.query.get(chapter.course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            resource = ResourceModel.query.filter_by(course_id=chapter_id, no=no).first()
            db.session.delete(resource)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
