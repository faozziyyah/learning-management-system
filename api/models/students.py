from ..utils import db

class Student(db.Model ):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    admission_no = db.Column(db.String(20))
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    courses = db.relationship('Course', backref='student_course', lazy='dynamic')
    score = db.relationship('Score', backref='teacher_score', lazy='dynamic')
    user = db.Column(db.Integer(), db.ForeignKey('users.id'))
    
    def __repr__(self):
        return f"<Student {self.id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()