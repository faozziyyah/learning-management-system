from ..utils import db

class User(db.Model ):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    email =  db.Column( db.String(100) , nullable=False , unique=True )
    username = db.Column(db.String(100), nullable=False, unique=True )
    password_hash = db.Column(db.Text() , nullable=False )
    is_staff = db.Column(db.Boolean(), default=False)
    students=db.relationship('Student', backref='students', lazy='True')
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)