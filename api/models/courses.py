from ..utils import db
from datetime import datetime

class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    teacher = db.Column(db.String(50), nullable=False, unique=True)
    students = db.relationship('Student', backref='student', lazy='dynamic')
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name