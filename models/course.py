from . import db


class CourseModel(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    teacher_id = db.Column(db.String(10))
    assistant_id = db.Column(db.String(10), nullable=True)
    time = db.Column(db.String(50))
    address = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=True)
