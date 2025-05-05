from flask import Flask, render_template, request, flash, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, UserMixin
from flask_mail import Mail, Message
from .extensions import bcrypt, init_app
from bson import ObjectId
# seting the environment
from dotenv import load_dotenv
import os
load_dotenv()

import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)
CORS(app) 
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

cloudinary.config( 
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'), 
    api_key=os.getenv('CLOUDINARY_API_KEY'), 
    api_secret=os.getenv('CLOUDINARY_API_SECRET'), 
    secure=True 
)

app.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_USERNAME')
)
mail = Mail(app)

# Initialize extensions
init_app(app)

# User class
class User(UserMixin):
    def __init__(self, user_dict):
        self.id = str(user_dict['_id'])  # Convert ObjectId to string
        self.username = user_dict['username']
        self.email_address = user_dict['email_address']
        self.role = user_dict['role']
        self.password = user_dict['password']

    def get_id(self):
        return str(self.id)  # Ensure we return string ID

# intatiate an login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from config.mdatabase import users_collection
    try:
        user = users_collection.find_one({'_id': ObjectId(user_id)})
        return User(user) if user else None
    except Exception as e:
        print("Error loading user:", str(e))
        return None

from application.apis import *
from application.admin_api import *