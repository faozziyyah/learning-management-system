from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, get_jwt_identity, current_user)
from ..models.teachers import Teacher
from ..models.users import User
from http import HTTPStatus
from ..utils import db

teacher_namespace = Namespace('teacher',description='a namespace for teacher')

teacher_model=teacher_namespace.model(
    'Teacher', {
    'id':fields.Integer(description='ID'),
    'name':fields.String(required=True, description="username"),
    'email':fields.String(required=True, description="name"),
    }
)

@teacher_namespace.route("/teachers")
class Teachers(Resource):
    @teacher_namespace.marshal_with(teacher_model)
    @teacher_namespace.doc(description="Retrieve All Teachers")
    @jwt_required()
    def get(self):
        """
        Get All Teachers
        """

        teachers = Teacher.query.all()
        return teachers, HTTPStatus.OK