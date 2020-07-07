from flask_wtf.csrf import CSRFProtect

from flask_login.login_manager import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman

# Build external Flask extensions

# We are building them in a separate file from spellr/__init__.py to
# make it easier to import the global variables, specifically the
# login_manager and db variables into other modules

csrf = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
talisman = Talisman()
