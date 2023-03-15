from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from ..models.students import Student
from ..models.users import User
from http import HTTPStatus
from ..utils import db

student_namespace = Namespace('students',description='a namespace for students')

student_model=student_namespace.model(
    'Student', {
    'id':fields.Integer(description='ID'),
    'admission_no':fields.Integer(description='Admission Number'),
    'name':fields.String(required=True, description="username"),
    'email':fields.String(required=True, description="name"),
    'course':fields.String(required=True, description="Course"),
    'score':fields.Integer(description='score'),
    }
)

@student_namespace.route('/students')
class StudentGetCreate(Resource):

    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="Get all students"
    )
    @jwt_required(refresh=True)
    def get(self):
        """
           Get all students
        """
        students=Student.query.all()

        return students, HTTPStatus.ok

    @student_namespace.expect(student_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="Creata a new student"
    )
    @jwt_required(refresh=True)
    def post(self):
        """
           Create a new student
        """
        username=get_jwt_identity()

        current_user=User.query.filter_by(username=username).first()

        data=student_namespace.payload

        new_student=Student(
            admission_no=data['admission_no'],
            name=data['name'],
            email=data['email'],
            course=data['course'],
            score=data['score'],
        )

        new_student.user=current_user

        new_student.save()

        return new_student, HTTPStatus.CREATED

@student_namespace.route('/students/<int:student_id>')
class GetUpdateDelete(Resource):

    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="Retrieve a student by ID"
    )
    @jwt_required(refresh=True)
    def get(self,student_id):
        """
           Retrieve a student by id
        """
        student=Student.get_by_id(student_id)

        return student, HTTPStatus.ok

    @student_namespace.expect(student_model)
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="Update a student"
    )
    @jwt_required()
    def put(self,student_id):
        """
           Update a student
        """
        student_to_update = Student.get_by_id(student_id)

        data=student_namespace.payload

        student_to_update.name=data['name']
        student_to_update.email=data['email']

        db.session.commit()

        return student_to_update, HTTPStatus.ok

    @jwt_required()
    @student_namespace.marshal_with(student_model)
    @student_namespace.doc(
        description="Deleta a student"
    )
    def delete(self,student_id):
        """
           Delete a student
        """
        student_to_delete = Student.get_by_id(student_id)

        student_to_delete.delete()

        return student_to_delete, HTTPStatus.ok
    
@student_namespace.route('/user/<int:user_id>/student/<int:student_id>/')
class GetStudentScore(Resource):

    def get(self,user_id,student_id):
        """
           Retrieve a student's score
        """
        pass
    
@student_namespace.route('/student/status/<int:student_id>')
class UpdateStudentStatus(Resource):

    def patch(self,student_id):
        """
           Update a student's status
        """
        pass