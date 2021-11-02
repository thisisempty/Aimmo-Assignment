from flask_mongoengine  import MongoEngine
from flask_bcrypt       import Bcrypt
from flask_restful      import Api
from flask_jwt_extended import JWTManager
from flask_cors         import CORS

from routes  import initialize_routes
from app     import get_app_with_config
from config  import Runconfig

app = get_app_with_config(Runconfig)
CORS(app)
db     = MongoEngine()
api    = Api(app)
bcrypt = Bcrypt(app)
jwt    = JWTManager(app)

db.init_app(app)

initialize_routes(api)

if __name__ == '__main__':
    app.run(host='0.0.0.0')