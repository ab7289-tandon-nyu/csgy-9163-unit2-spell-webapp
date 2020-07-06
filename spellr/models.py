from spellr.extensions import db
from werkzeug.security import check_password_hash


class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), index=False, unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=True)
    two_factor = db.Column(db.String(10), index=False, unique=False, nullable=False)

    def check_password(self, value):
        return check_password_hash(self.password, value)

    def check_two_factor(self, value):
        return self.two_factor == value

    def __repr__(self):
        return f"<User {self.username}>"
