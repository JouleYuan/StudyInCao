from . import db


class HomeworkStudentModel(db.Model):
    __tablename__ = 'homework_student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    homework_id = db.Column(db.Integer)
    student_id = db.Column(db.String(10))
    text = db.Column(db.Text, nullable=True)
    file = db.Column(db.String(10), nullable=True)
    grade = db.Column(db.Integer, nullable=True)
