from . import db


class CourseStudentModel(db.Model):
    __tablename__ = 'course_student'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer)
    student_id = db.Column(db.String(10))
    grade = db.Column(db.Integer, nullable=True)
