from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.reply import ReplyModel
from common import code, pretty_result, file
from common.auth import verify_student_token, verify_teacher_token, verify_admin_token
from werkzeug.datastructures import FileStorage

class Replies(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()
    def get(self, post_id):
        try:
            data = []
            replies = ReplyModel.query.filter_by(post_id=post_id).all()
            for reply in replies:
                data.append({
                    'reply_id': reply.id,
                    'user_id': reply.user_id,
                    'time': str(reply.time),
                    'content': reply.content
                })
            
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
    
    def post(self, post_id):
        try:
            if (verify_student_token(self.token_parser) or verify_teacher_token(self.token_parser)) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)
            self.parser.add_argument('user_id', type=int, location='args')
            self.parser.add_argument('content', type=str, location='args')
            args = self.parser.parse_args()

            reply = ReplyModel(
                post_id = post_id,
                content = args['content'],
                user_id = args['user_id']
            )
            db.session.add(reply)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

class Reply(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()

    def delete(self, reply_id):
        if (verify_admin_token(self.token_parser) or verify_teacher_token(self.token_parser)) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        try:
            reply = PostModel.query.get(reply_id)
            db.session.delete(reply)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
