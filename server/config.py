import os
import datetime
import json
from flask_cors import CORS
from flask import Flask, request, send_from_directory
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from environs import Env
import environs
from flask_bcrypt import Bcrypt
from flasgger import Swagger

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    env = Env()
    env.read_env()

    try: 
        db_user = env("DB_USERNAME")
        db_pw = env("DB_PASSWORD")

    except environs.EnvError:
        print("*******************************************************")
        print("DB_USERNAME or DB_PASSWORD environment variable not set")
        print("*******************************************************")

    is_docker = None
    try:
        is_docker = env("IS_DOCKER")
        # db_ip = env("DB_IP")
    except environs.EnvError:
        print("is_docker or dp_ip not set")
    else:
        print("isdocker: " + str(is_docker))

    if not (is_docker == None):
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_pw}@host.docker.internal:3306/cradle' # ex: 'mysql+pymysql://root:123456@localhost:3306/mydb'
    else:
        SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{db_user}:{db_pw}@localhost:3306/cradle' # ex: 'mysql+pymysql://root:123456@localhost:3306/mydb'
    
    print("SQLALCHEMY_DATABASE_URI: " + SQLALCHEMY_DATABASE_URI)

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test-cradle.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT_SECRET_KEY= os.environ.get('SECRET')
    JWT_SECRET_KEY = 'very secret'
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=7)

class JSONEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, datetime.datetime):
            return str(o)
        return json.JSONEncoder.default(self, o)


FLASK_APP = 'app.py'
FLASK_DEBUG=1

app = Flask(__name__, static_folder='../client/build')
app.config['SWAGGER'] = {
    'openapi': '3.0.2'
}
swagger = Swagger(app)

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

CORS(app)
api = Api(app)
app.config.from_object(Config)

flask_bcrypt = Bcrypt(app)
jwt = JWTManager(app)
app.json_encoder = JSONEncoder

db = SQLAlchemy(app)
migrate = Migrate(app, db)
ma = Marshmallow(app)
