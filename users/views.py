import datetime, re

from flask              import request
from flask_jwt_extended import create_access_token
from flask_restful      import Resource
from mongoengine.errors import NotUniqueError, ValidationError

from database.models import User


class SignUpApi(Resource):
    def post(self):
        data = request.get_json()

        EMAIL_REGEX    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        PASSWORD_REGEX = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

        try:
            email    = data['email']
            password = data['password']

            if not re.match(EMAIL_REGEX, email):
                return {'message' : 'INVALID_EMAIL'}, 400

            if not re.match(PASSWORD_REGEX, password):
                return {'message' : 'INVALID_PASSWORD'}, 400

            user = User(**data)
            user.hash_password()
            user.save()
            
            return {'message' : 'SUCCESS'}, 201
        
        except ValidationError:
            return {'message' : 'VALIDATION_ERROR'}, 400
            
        except NotUniqueError:
            return {'message' : 'ALREADY_EXIST'}, 400

class SignInApi(Resource):
    def get(self):
        try :
            data = request.get_json()

            user       = User.objects.get(email=data.get('email'))
            authorized = user.check_password(data.get('password'))

            if not authorized:
                return {'message' : 'INVALID_PASSWORD_OR_EMIAL'}, 401
            
            expires      = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)

            return {'token' : access_token}, 200

        except ValidationError:
            return {'message' : 'VALIDATION_ERROR'}, 400
        
        except User.DoesNotExist:
            return {'message' : 'DOES_NOT_EXISTS'}, 404



