from flask_wtf.csrf import CSRFProtect

from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman


csrf = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
talisman = Talisman()
