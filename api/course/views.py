from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, current_user)
from ..models.courses import Course
from ..models.students import Student
from ..models.scores import Grade
from ..models.admin import Admin
from http import HTTPStatus
from ..utils import db

course_namespace = Namespace('course',description='a namespace for course')

course_model=course_namespace.model(
    'Course', {
    'id':fields.Integer(description='ID'),
    'course_name': fields.String(required=True, description='Course Name', enum=['FrontEnd', 'BackEnd', 'Cloud']),
    "teacher": fields.String(description="Teacher Full Name"),
    }
)

@course_namespace.expect(course_model)
@course_namespace.marshal_with(course_model)
@course_namespace.doc(description="Course Creation (Admin Only)")
@jwt_required()
def post(self):
        """
        Admin: Create a Course
        """
        if current_user.is_admin:
            data = course_namespace.payload

            new_course = Course(
                name=data["name"],
                code=data["code"],
                credit=data["credit"],
                teacher_id=data["teacher_id"],
                department_id=data["department_id"],
                created_by=current_user.username,
            )

            new_course.save()
            new_course = new_course.id

            return new_course, HTTPStatus.CREATED

@course_namespace.route("/courses")
class Courses(Resource):

    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description="Retrieve All courses")
    @jwt_required()
    def get(self):
        """
        Get All Courses
        """

        courses = {
            'FrontEnd': 'FrontEnd Engineering',
            'BackEnd': 'BackEnd Engineering',
            'Cloud': 'Cloud Engineering'
        }
        return courses, HTTPStatus.OK

@course_namespace.route('/student/get_course')
class GetCourseBySpecificStudent(Resource):
    @course_namespace.marshal_with(course_model)
    @jwt_required()
    def get(self):
        '''
            Get course for a user through their id
        '''
        email = get_jwt_identity()
        current_user = Student.query.filter_by(email=email).first()
        current_user_id = current_user.id
        courses = Course.query.filter_by(
            student=current_user_id).all()
        course_name = courses
        return course_name, HTTPStatus.OK    

@course_namespace.route("/<int:course_id>/students")
class GetCourseStudents(Resource):
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(description="Retrieve Specific Course Students (Admin Only)", params=dict(course_id="Course ID"))
    @jwt_required()
    def get(self, course_id):
        """
        Admin: Get All Students Offering Specific Course
        """
        if current_user.is_admin:
            if (course_id):
                course_students = course_students(course_id)
                return course_students, HTTPStatus.ok