from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# generated key in python via secrets.token_hex(16)
# secret key serves as protection against modifying cookies and such
app.config['SECRET_KEY'] = '34b1d628cc7a4a647d3900624aa2bf91'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from gamerscreenshots import routes