from ..utils import db
from datetime import datetime

class Grade(db.Model):

    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<Grade {self.id}>"