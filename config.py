from flask import Flask
from flask_login import LoginManager
from app import models, routes

app = Flask(__name__)
app.config.from_object('config.Config')

login_manager = LoginManager()
login_manager.init_app(app)



