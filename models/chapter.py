from . import db


class ChapterModel(db.Model):
    __tablename__ = 'chapter'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(db.Integer)
    no = db.Column(db.Integer)
    title = db.Column(db.String(50))
