from . import db
from sqlalchemy.sql import func


class HomeworkModel(db.Model):
    __tablename__ = 'homework'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_id = db.Column(db.Integer)
    title = db.Column(db.String(50))
    content = db.Column(db.Text, nullable=True)
    time = db.Column(db.DateTime, server_default=func.now(), default=func.now())
    deadline = db.Column(db.DateTime)
