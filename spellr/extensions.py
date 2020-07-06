from flask_wtf.csrf import CSRFProtect

from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy


csrf = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
