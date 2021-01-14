from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.post import PostModel
from common import code, pretty_result, file
from common.auth import verify_admin_token, verify_login_token
from werkzeug.datastructures import FileStorage

class Posts(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()
    def get(self, course_id):
        try:
            data = []
            posts = PostModel.query.filter_by(course_id=course_id).all()
            for post in posts:
                data.append({
                    'post_id': post.id, 
                    'course_id': post.course_id,
                    'user_id': post.user_id,
                    'time': str(post.time),
                    'title': post.title,
                    'content': post.content
                })
            
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
    
    def post(self, course_id):
        try:
            if verify_login_token(self.token_parser) is False:
                return pretty_result(code.AUTHORIZATION_ERROR)
            self.parser.add_argument('user_id', type=int, location='args')
            self.parser.add_argument('title', type=str, location='args')
            self.parser.add_argument('content', type=str, location='args')
            args = self.parser.parse_args()

            post = PostModel(
                course_id = course_id, 
                title = args['title'],
                user_id = args['user_id'],
                content = args['content']
            )
            db.session.add(post)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

        

class Post(Resource):
    def __init__(self):
        self.parser = RequestParser()
        self.token_parser = RequestParser()
    
    def get(self, post_id):
        try:
            post = PostModel.query.get(post_id)
            data = {
                'post_id': post.id, 
                'course_id': post.course_id,
                'user_id': post.user_id,
                'time': str(post.time),
                'title': post.title,
                'content': post.content
            }
            return pretty_result(code.OK, data=data)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)
        
    def delete(self, post_id):
        if verify_login_token(self.token_parser) is False:
            return pretty_result(code.AUTHORIZATION_ERROR)

        try:
            post = PostModel.query.get(post_id)
            db.session.delete(post)
            db.session.commit()
            return pretty_result(code.OK)
        except SQLAlchemyError as e:
            print(e)
            db.session.rollback()
            return pretty_result(code.DB_ERROR)

