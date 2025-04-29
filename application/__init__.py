from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
# seting the environment
from dotenv import load_dotenv
import os
load_dotenv()

import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)
CORS(app) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mystore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

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
)
mail = Mail(app)


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# intatiate an login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from application.models import *
from application.apis import *