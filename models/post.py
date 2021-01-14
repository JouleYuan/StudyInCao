from . import db
from sqlalchemy.sql import func


class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer)
    user_id = db.Column(db.String(10))
    time = db.Column(db.DateTime, server_default=func.now())
    title = db.Column(db.String(50))
    content = db.Column(db.String(255))
    file = db.Column(db.String(255))
