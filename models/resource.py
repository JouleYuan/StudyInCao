from . import db


class ResourceModel(db.Model):
    __tablename__ = 'resource'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_id = db.Column(db.Integer)
    title = db.Column(db.String(50))
    file = db.Column(db.String(255), nullable=True)
    content = db.Column(db.Text, nullable=True)
