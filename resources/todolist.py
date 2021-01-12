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
from operator import itemgetter


class TodoList(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def get(self, student_id):
        """if verify_id_token(self.token_parser, student_id) is False \
                and verify_admin_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)"""

        try:
            data = []
            homework_students = HomeworkStudentModel.query.filter_by(student_id=student_id).all()
            for homework_student in homework_students:
                if homework_student.text is None and homework_student.file is None:
                    homework = HomeworkModel.query.get(homework_student.id)
                    if homework.deadline > datetime.datetime.now():
                        chapter = ChapterModel.query.get(homework.chapter_id)
                        course = CourseModel.query.get(chapter.course_id)
                        data.append({
                            'coursename': course.name,
                            'mission': homework.title,
                            'missiontype': '作业',
                            'ddl': homework.deadline
                        })
            data.sort(key=itemgetter('ddl'))
            for d in data:
                d['ddl'] = str(d['ddl'])
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
