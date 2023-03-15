import unittest
from .. import create_app
from ..config.config import config_dict
from ..models.students import Student
from ..utils import db
from flask_jwt_extended import create_access_token


class OrderTestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(config=config_dict['testing'])
        self.appctx=self.app.app_context()

        self.appctx.push()

        self.client=self.app.test_client()

        db.create_all()


    def tearDown(self):
        db.drop_all()

        self.app=None

        self.appctx.pop()

        self.client=None


    def test_get_all_students(self):

        token=create_access_token(identity='testuser')

        headers={
            "Authorization":f"Bearer {token}"
        }

        response=self.client.get('/students/students/',headers=headers)

        assert response.status_code == 200

        assert response.json == []


    def test_create_student(self):
        data={
            "name":"Grace",
            "email":"grace_jam@gmail.com",
            "admission_no":"001"
        }

        token=create_access_token(identity='testuser')

        headers={
            "Authorization":f"Bearer {token}"
        }


        response=self.client.post('/students/students/',json=data,headers=headers)


        assert response.status_code == 201

        students= Student.query.all()

        assert len(students) == 1