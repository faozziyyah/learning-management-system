from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, current_user)
from ..models.courses import Course
from ..models.users import User
from ..models.students import Student
from ..models.scores import Grade
from ..models.admin import Admin
from http import HTTPStatus
from ..utils import db
from flask import request

grades_namespace = Namespace('grades',description='a namespace for grades')

grades_model=grades_namespace.model(
    'Grades', {
    'id':fields.Integer(description='ID'),
    'score': fields.String(required=True, description='student score')
    }
)

@grades_namespace.route('/grade/student/<int:student_id>')
class GradeStudentById(Resource):
    @grades_namespace.expect(grades_model)
    @grades_namespace.marshal_with(grades_model)
    @jwt_required()
    def post(self, student_id):
        '''
            Grading for Students By Id
        '''

        user_allowed = get_jwt_identity()
        author_admin = Admin.query.filter_by(email=user_allowed).first()
        author_student = Student.query.filter_by(email=user_allowed).first()
        data = request.get_json()
        user_id = Student.query.filter_by(id=student_id).first()
        user_id_id = user_id.id
        grades = Grade.query.filter_by(student=user_id_id).all()
        try:
            if len(grades) >= 1:
                return {'message': 'You are not allowed to grade this student again'}, HTTPStatus.UNAUTHORIZED
            else:
                if author_admin:
                    set_grade = Grade(score=data['score'])
                    set_grade.student = user_id_id
                    print(set_grade.student)
                    set_grade.save()
                    return set_grade, HTTPStatus.CREATED
                elif author_student:
                    return {"message": "UNAUTHORIZED"}, HTTPStatus.UNAUTHORIZED
        except AttributeError:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND

@grades_namespace.route('/grade/student')
class GradeOfStudent(Resource):
    @grades_namespace.marshal_with(grades_model)
    @jwt_required()
    def get(self):
        '''
            Get Grades of Students by the student
        '''
        user_allowed = get_jwt_identity()
        user_id = Student.query.filter_by(email=user_allowed).first()
        user_id_grade = user_id.grade

        return user_id_grade, HTTPStatus.OK