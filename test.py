import unittest, json, mongoengine

from flask_bcrypt       import generate_password_hash
from flask_restful      import Api
from flask_jwt_extended import JWTManager

from routes          import initialize_routes
from app             import get_app_with_config
from database.models import User
from config          import TestConfig

class UserUnitTest(unittest.TestCase):
    
    def setUp(self):
        self.app = get_app_with_config(TestConfig)
        api = Api(self.app)
        jwt = JWTManager(self.app)
        initialize_routes(api)
        self.db = mongoengine.connect('testdb')
        User(
            email="test1231@abc.com",
            password=generate_password_hash("Test123!"),
            nickname="jen"
        ).save()
        self.client = self.app.test_client()

    
    def tearDown(self):
        User.drop_collection()
        self.db.close()
        
    def test_signup_success(self):
        data = {
            "email":"test@abc.com",
            "password":"Test123!",
            "nickname":"홍길동"
        }
        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json,{
            'message' : 'SUCCESS'
        })
        
    
    def test_signup_fail_not_unique_error(self):
        data = {
            "email":"test1231@abc.com",
            "password":"Test123!",
            "nickname":"jen"
        }
        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,{
            'message' : 'ALREADY_EXIST'
        })

    def test_signup_fail_validation_error(self):
        data = {
            "email":"test@abc.com",
            "password":"Test123!",
        }
        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,{
            'message' : 'VALIDATION_ERROR'
        })

    def test_signup_fail_invalid_email(self):
        data = {
            "email":"testabc.com",
            "password":"Test123!",
            "nickname":"홍길동"
        }
        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,{
            'message' : 'INVALID_EMAIL'
        })

    def test_signup_fail_invalid_password(self):
        data = {
            "email":"test@abc.com",
            "password":"test123",
            "nickname":"홍길동"
        }
        response = self.client.post('/users/signup', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json,{
            'message' : 'INVALID_PASSWORD'
        })
    
    def test_signin_success(self):
        data = {
            "email":"test1231@abc.com",
            "password":"Test123!",
        }
        client = self.app.test_client()
        response = client.get('/users/signin', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        

if __name__ == '__main__':
    
    unittest.main()
