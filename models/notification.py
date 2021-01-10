from . import db
from sqlalchemy.sql import func


class NotificationModel(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    student_id = db.Column(db.String(10))
    content_type = db.Column(db.String(20))
    content_title = db.Column(db.String(50))
    state = db.Column(db.Integer)
    time = db.Column(db.DateTime, server_default=func.now())
    is_read = db.Column(db.Integer, default=0, server_default='0')
