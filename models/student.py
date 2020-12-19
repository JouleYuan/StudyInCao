from . import db


class StudentModel(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(15))
    gender = db.Column(db.BOOLEAN)
    class_name = db.Column(db.String(50))
    email = db.Column(db.String(50), nullable=True)
    avatar = db.Column(db.BOOLEAN)
