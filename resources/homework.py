from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.course import CourseModel
from models.chapter import ChapterModel
from models.homework import HomeworkModel
from models.course_student import CourseStudentModel
from models.homework_student import HomeworkStudentModel
from models.notification import NotificationModel
from models.student import StudentModel
from common import code, pretty_result, file
from common.auth import verify_id_token, verify_student_token, verify_admin_token
import datetime
from werkzeug.datastructures import FileStorage


class AllHomework(Resource):
    def get(self):
        try:
            homeworks = HomeworkModel.query.all()
            data = [
                {
                    'id': homework.id,
                    'chapter_id': homework.chapter_id,
                    'title': homework.title,
                    'content': homework.content,
                    'time': str(homework.time),
                    'deadline': str(homework.deadline)
                }
                for homework in homeworks
            ]
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class CourseHomework(Resource):
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
                homeworks = HomeworkModel.query.filter_by(chapter_id=chapter.id).all()
                chapter_data['resources'] = [
                    {
                        'id': homework.id,
                        'title': homework.title,
                        'content': homework.content,
                        'time': str(homework.time),
                        'deadline': str(homework.deadline)
                    }
                    for homework in homeworks
                ]
                data.append(chapter_data)
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class ChapterHomework(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, chapter_id):
        try:
            homeworks = HomeworkModel.query.filter_by(chapter_id=chapter_id).all()
            data = [
                {
                    'id': homework.id,
                    'title': homework.title,
                    'content': homework.content,
                    'time': str(homework.time),
                    'deadline': str(homework.deadline)
                }
                for homework in homeworks
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
            self.parser.add_argument('deadline', type=int, location="args")
            args = self.parser.parse_args()

            homework = HomeworkModel(
                chapter_id=chapter_id,
                title=args['title'],
                content=args['content'],
                deadline=datetime.datetime.fromtimestamp(args['deadline'])
            )
            db.session.add(homework)

            students = CourseStudentModel.query.filter_by(course_id=course.id).all()
            for student in students:
                homework_student = HomeworkStudentModel(
                    homework_id=homework.id,
                    student_id=student.student_id,
                )
                db.session.add(homework_student)
                notification = NotificationModel(
                    student_id=student.student_id,
                    content_type="作业",
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


class IdHomework(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, id):
        try:
            homework = HomeworkModel.query.get(id)
            data = {
                'chapter_id': homework.chapter_id,
                'title': homework.title,
                'content': homework.content,
                'time': str(homework.time),
                'deadline': str(homework.deadline)
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def put(self, id):
        try:
            homework = HomeworkModel.query.get(id)
            chapter = ChapterModel.query.get(homework.chapter_id)
            course = CourseModel.query.get(chapter.course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            self.parser.add_argument('title', type=str, location="args")
            self.parser.add_argument('content', type=str, location="form")
            self.parser.add_argument('deadline', type=int, location="args")
            args = self.parser.parse_args()

            if args['title'] is not None:
                homework.title = args['title']
            if args['content'] is not None:
                homework.content = args['content']
            if args['deadline'] is not None:
                homework.deadline = args['deadline']
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

    def delete(self, id):
        try:
            homework = HomeworkModel.query.get(id)
            chapter = ChapterModel.query.get(homework.chapter_id)
            course = CourseModel.query.get(chapter.course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            db.session.delete(homework)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class UploadHomework(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def put(self, homework_id, student_id):
        if (verify_student_token(self.token_parser) and verify_id_token(self.token_parser, student_id)) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        self.parser.add_argument('text', type=str, location="form")
        self.parser.add_argument('file', type=FileStorage, location="files")
        args = self.parser.parse_args()

        try:
            homework_student = HomeworkStudentModel.query. \
                filter_by(homework_id=homework_id, student_id=student_id).first()
            if args['text'] is not None:
                homework_student.text = args['text']
            file.upload_homework(args['file'], homework_student)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class ReviewHomework(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def put(self, homework_id, student_id):
        try:
            homework = HomeworkModel.query.get(homework_id)
            chapter = ChapterModel.query.get(homework.chapter_id)
            course = CourseModel.query.get(chapter.course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            self.parser.add_argument('grade', type=int, location="args")
            args = self.parser.parse_args()

            homework_student = HomeworkStudentModel.query. \
                filter_by(homework_id=homework_id, student_id=student_id).first()
            homework_student.grade = args['grade']
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class HomeworkGrade(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, homework_id):
        try:
            homework = HomeworkModel.query.get(homework_id)
            chapter = ChapterModel.query.get(homework.chapter_id)
            course = CourseModel.query.get(chapter.course_id)
            if verify_id_token(self.token_parser, course.teacher_id) is False \
                    and verify_id_token(self.token_parser, course.assistant_id) is False \
                    and verify_admin_token(self.token_parser) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)

            data = []
            homework_students = HomeworkStudentModel.query.filter_by(homework_id=homework_id).all()
            for homework_student in homework_students:
                file = None
                if homework_student.file is not None:
                    file = 'file/homework/' + str(homework_student.id)
                student = StudentModel.query.get(homework_student.student_id)
                data.append({
                    'id': student.id,
                    'name': student.name,
                    'gender': student.gender,
                    'class_name': student.class_name,
                    'text': homework_student.text,
                    'file': file,
                    'grade': homework_student.grade
                })
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)


class StudentHomeworkGrade(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, homework_id, student_id):
        if (verify_student_token(self.token_parser) and verify_id_token(self.token_parser, student_id)) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        try:
            homework_student = HomeworkStudentModel.query.\
                filter_by(homework_id=homework_id, student_id=student_id).first()
            data = {'grade': homework_student.grade}
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
