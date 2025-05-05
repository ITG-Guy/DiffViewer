# IMPORT modules for flask
import os
from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson.objectid import ObjectId

# User 모델과 로딩 함수를 MongoDB 스키마에 맞게 수정해야 함
from .mongo import mongo
from .constants import *

# DB Specification(Mongo DB)
app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'app/static'))
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default-secret-key-if-not-set')
# MongoDB Set-up, For example, the format is like 'mongodb://localhost:27017/myDatabase'.
# (MongoDB 설정, 예를 들어 'mongodb://localhost:27017/myDatabase' 형식으로 설정)
app.config['MONGO_URI'] = os.getenv('MONGO_URI', f'mongodb://{DB_DOMAIN_NAME}:{DB_DOMAIN_PORT}/{DB_NAME}')

# Browser could block the request from another domain for security.
# For example, Client(Front-end) is executed on localhost:3000 and API Server is running on localhost:5000,
# when Client send certain request to server,browser could block this.
# (That's not your partner!)
# In this case, flask_cors offers work-around method for CORS policy.

# from flask_cors import CORS
# CORS(app)

# mongo = PyMongo(app)
mongo.init_app(app)
from app import routes, models  # 나머지 import는 나중에
from .models import User

# Member manage module 

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    # Search the user with a ObjectId for MongoDB
    # (MongoDB의 ObjectId를 사용하여 사용자 검색)
    user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if user_data:
        return User(user_data['username'], user_data['email'], user_data['password_hash'], user_data['_id'])
    return None