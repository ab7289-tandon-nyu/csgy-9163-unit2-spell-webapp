from spellr.extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

role_association = db.Table(
    "user_role_mtom",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
)


class User(db.Model, UserMixin):
    """Data model for user accounts."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), index=False, unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=True)
    two_factor = db.Column(db.String(10), index=False, unique=False, nullable=False)
    roles = db.relationship(
        "Role",
        secondary=role_association,
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )

    def set_password(self, password):
        """ convenience function to generate the hashed user password """
        self.password = generate_password_hash(password)

    def check_password(self, value):
        """ convenience function to check that the supplied password matches the hash """
        return check_password_hash(self.password, value)

    def check_two_factor(self, value):
        return self.two_factor == value

    def __repr__(self):
        return f"<User {self.username}>"


class Role(db.Model):
    """Data model for role records."""

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
