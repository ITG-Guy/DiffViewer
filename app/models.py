# 1) Define Your DB models
# 2) Implement feature for DB CRUD

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

import os
import sys
# Get the current_dir path and add it to sys.path if it is not in it.
# (현재 스크립트 파일의 디렉토리 경로를 구합니다.)
current_dir = os.path.dirname(os.path.abspath(__file__))
if not current_dir in sys.path:
    sys.path.append(current_dir)
# Same as parent_dir
# (현재 디렉토리의 부모 디렉토리를 sys.path에 추가합니다.)
parent_dir = os.path.dirname(current_dir)
if not parent_dir in sys.path:
    sys.path.append(parent_dir)

# Now, with a relative path, import is available.
# (이제 상대경로로 import가 가능합니다.)
from .mongo import mongo
from pymongo import MongoClient
from constants import *

#### 0) User Model

class User(UserMixin):
    def __init__(self, username, email, password, _id):
        self.username = username
        self.email = email
        if password:
            self.password_hash = generate_password_hash(password)
        else:
            self.password_hash = None
        self._id = _id

    @staticmethod
    def validate_login(password_hash, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(password_hash, password)

    @classmethod
    def get(cls, user_id):
        # Find and return user data based on user_id.
        # (MongoDB에서 사용자 ID로 사용자 정보를 조회)
        user_data = mongo.db.users.find_one({'_id': user_id})
        if not user_data:
            return None
        return cls(user_data['username'], user_data['email'], user_data['password_hash'], user_data['_id'])

    def get_id(self):
        # Return user _id
        # (MongoDB의 사용자 문서 ID 반환)
        return str(self._id)
    
    @property
    def is_authenticated(self):
        # Check whether the user is authenticated or not.
        # (이 메소드는 사용자가 인증되었는지 확인합니다.)
        return True

    @property
    def is_active(self):
        # Check whether the user is active or not
        # (이 메소드는 계정이 활성화 상태인지 확인합니다.)
        return True

    @property
    def is_anonymous(self):
        # Check whether anonymus or not. Not activated feature.(it means invalid.)
        # (실제 사용자는 항상 익명이 아니므로 False를 반환합니다.)
        return False

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        user_data = {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
        }
        if self._id:  # if there i already user, then just update the user_data.(사용자가 이미 존재하면 업데이트)
            mongo.db.users.update_one({'_id': self._id}, {'$set': user_data})
        else:  # if new user, insert the user_data (새 사용자면 삽입)
            result = mongo.db.users.insert_one(user_data)
            self._id = result.inserted_id


    def to_json(self):
        # return the user_data with a form of dict type.(Mongo DB stores data with a json type.)
        # (이 메소드는 사용자 객체를 MongoDB 문서 형식으로 변환합니다.)
        return {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
        }

    @staticmethod
    def find_by_username(username):
        user_data = mongo.db.users.find_one({'username': username})
        if user_data:
            return User(user_data['username'], user_data['email'], password_hash=user_data.get('password_hash'))
        return None

    @staticmethod
    def find_by_id(user_id):
        user_data = mongo.db.users.find_one({'_id': user_id})
        if user_data:
            return User(user_data['username'], user_data['email'], password_hash=user_data.get('password_hash'))
        return None
