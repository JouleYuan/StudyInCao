from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.notification import NotificationModel
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
            notifications = NotificationModel.query.filter_by(student_id=student_id).all()
            data = [{
                'id': notification.id,
                'content_type': notification.content_type,
                'content_title': notification.content_title,
                'state': notification.state,
                'time': notification.time,
                'is_read': notification.is_read,
            } for notification in notifications]
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
