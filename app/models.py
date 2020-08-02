from app.extensions import db
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from sqlalchemy import event

# many-to-many association table linking users and their roles
role_association = db.Table(
    "user_role_mtom",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id"), primary_key=True),
)


class User(db.Model, UserMixin):
    """Data model for user accounts."""

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=True)
    two_factor = db.Column(db.String(11), unique=False, nullable=False)
    roles = db.relationship(
        "Role",
        secondary=role_association,
        lazy="subquery",
        backref=db.backref("users", lazy=True),
    )
    questions = db.relationship("Question", back_populates="user", lazy=True)
    auth_histories = db.relationship("AuthHistory", backref="user", lazy=True)

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


@event.listens_for(User, "init")
def receive_init(target, args, kwargs):
    """listen for the User model's init event"""

    # when a new user is created, add the 'user' role to them by default
    user_role = Role.query.filter_by(name="user").first()
    target.roles.append(user_role)


class Role(db.Model):
    """Data model for role records."""

    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)


class Question(db.Model):
    """Data model for user's previous questions."""

    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    result = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="questions")


class AuthHistory(db.Model):
    """Data model for login and logout times for a user"""

    __tablename__ = "auth_histories"
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.DateTime)
    logout = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
