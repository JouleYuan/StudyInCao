from . import db


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(10), primary_key=True)
    password = db.Column(db.String(32))
    question = db.Column(db.String(50))
    answer = db.Column(db.String(32))
    is_student = db.Column(db.BOOLEAN)
    is_teacher = db.Column(db.BOOLEAN)
    is_assistant = db.Column(db.BOOLEAN)
    is_admin = db.Column(db.BOOLEAN)
