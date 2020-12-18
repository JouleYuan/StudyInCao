from . import db


class TeacherModel(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(15))
    gender = db.Column(db.BOOLEAN)
    school = db.Column(db.String(50))
    title = db.Column(db.String(30))
    address = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text)
    avatar = db.Column(db.LargeBinary(length=(2**24)-1), nullable=True)
