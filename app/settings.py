"""Application config

Environment variables will take precedence
for debugging create a top level .env file"""
from environs import Env

env = Env()
env.read_env()

ENV = env.str("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SQLALCHEMY_DATABASE_URI = env.str("DATABASE_URL")
SECRET_KEY = env.str("SECRET_KEY")
SQLALCHEMY_TRACK_MODIFICATIONS = False
# sets the SameSite cookie option to restrict how cookies are
# sent with requests from external sites
SESSION_COOKIE_SAMESITE = env.str("SESSION_COOKIE_SAMESITE", default="Lax")

ADMIN_USER = env.str("ADMIN_USER")
ADMIN_PASS = env.str("ADMIN_PASS")
ADMIN_TF = env.str("ADMIN_TF")

TEST_USER = env.str("TEST_USER")
TEST_PASS = env.str("TEST_PASS")
TEST_TF = env.str("TEST_TF")
