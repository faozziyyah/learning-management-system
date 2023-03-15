from flask import Flask
from flask_restx import Api
from .students.views import student_namespace
from .auth.views import auth_namespace
from .config.config import config_dict
from .utils import db
from .models.students import Student
from .models.users import User
from .models.courses import Course
from .models.scores import Grade
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed

def create_app(config=config_dict['dev']):

    app=Flask(__name__)

    app.config.from_object(config)

    authorizations={
        "Bearer Auth":{
            'type':"apiKey",
            'in':"header",
            'name':"Authorization",
            'description':"Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }

    db.init_app(app)

    jwt=JWTManager(app)

    migrate = Migrate(app, db)
    
    api=Api(app,
            title="Learning Management System API",
            description="A rest API for a Learning management system",
            authorization=authorizations,
            security="Bearer Auth"
        )

    @api.errorhandler(NotFound)
    def not_found(error):
        return {"error": "Not Found"}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {"error": "Method Not Allowed"}, 404
    
    api.add_namespace(student_namespace)
    api.add_namespace(auth_namespace,path='/auth')

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'User': User,
            'Student': Student
        }

    return app