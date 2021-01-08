from . import db
from sqlalchemy.sql import func

class ReplyModel(db.Model):
    __tablename__ = 'reply'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.String(10))
    time = db.Column(db.DateTime, server_default = func.now())
    content = db.Column(db.String(255))
    file = db.Column(db.String(255))
