from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.course import CourseModel
from models.chapter import ChapterModel
from common import code, pretty_result
from common.auth import verify_id_token


class AllChapter(Resource):
    def get(self):
        try:
            chapters = ChapterModel.query.all()
            data = [
                {
                    'id': chapter.id,
                    'course_id': chapter.course_id,
                    'no': chapter.no,
                    'title': chapter.title
                }
                for chapter in chapters
            ]
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class CourseChapter(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, course_id):
        try:
            chapters = ChapterModel.query.filter_by(course_id=course_id).all()
            data = [
                {
                    'id': chapter.id,
                    'course_id': chapter.course_id,
                    'no': chapter.no,
                    'title': chapter.title
                }
                for chapter in chapters
            ]
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class Chapter(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, course_id, no):
        try:
            chapter = ChapterModel.query.filter_by(course_id=course_id, no=no).first()
            data = {
                'id': chapter.id,
                'course_id': chapter.course_id,
                'no': chapter.no,
                'title': chapter.title
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def post(self, course_id, no):
        try:
            course = CourseModel.query.get(course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            self.parser.add_argument('title', type=str, location="args")
            args = self.parser.parse_args()

            chapter = ChapterModel.query.filter_by(course_id=course_id, no=no).first()
            if chapter is not None:
                return pretty_result(code.DB_ERROR)

            chapter = ChapterModel(
                course_id=course_id,
                no=no,
                title=args['title']
            )
            db.session.add(chapter)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def put(self, course_id, no):
        try:
            course = CourseModel.query.get(course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            self.parser.add_argument('title', type=str, location="args")
            args = self.parser.parse_args()

            chapter = ChapterModel.query.filter_by(course_id=course_id, no=no).first()
            chapter.title = args['title']
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def delete(self, course_id, no):
        try:
            course = CourseModel.query.get(course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            chapter = ChapterModel.query.filter_by(course_id=course_id, no=no).first()
            db.session.delete(chapter)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
