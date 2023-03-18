from ..utils import db
from datetime import datetime

class Grade(db.Model):

    __tablename__ = "grades"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    student = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_code = db.Column(db.String(6), unique=False, nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))
    score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    def __repr__(self):
        return f"<Student ID: {self.student_id}, Course ID: {self.course_id}, Grade: {self.score}>"
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    def save(self):
        db.session.add(self)
        db.session.commit()