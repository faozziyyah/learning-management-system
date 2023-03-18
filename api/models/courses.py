from ..utils import db
from datetime import datetime
from enum import Enum

class courseList(Enum):
    FrontEnd = 'FrontEnd'
    BackEnd = 'BackEnd'
    Cloud = 'Cloud'

class Course(db.Model):

    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(courseList), nullable=False, default='')
    teacher = db.Column(db.Integer, nullable=False)
    student = db.Column(db.Integer(), db.ForeignKey('student.id'))
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Name %r>' % self.name
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    @classmethod
    def delete_student_course(cls, id):
        model = cls.query.get(id)
        if not model:
            return False
        db.session.delete(model)
        db.session.commit()
        return True