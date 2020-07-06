from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError
import phonenumbers
from wtforms.validators import DataRequired, Length
from werkzeug.security import check_password_hash

from spellr.db import get_db


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()], id="uname")
    password = PasswordField("Password", validators=[DataRequired()], id="pword")
    two_factor = StringField(
        "Two Factor Auth Device", id="2fa", validators=[DataRequired()]
    )  # optionally could also looking at using wtforms.fields.html5.TelField

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False

        db = get_db()
        self.user = db.execute(
            "SELECT * FROM user WHERE username = ?", (self.username.data,)
        ).fetchone()

        if not self.user or not check_password_hash(
            self.user["password"], self.password.data
        ):
            self.username.errors.append("Incorrect username or password")
            return False

        if not self.user["two_factor"] == self.two_factor.data:
            self.two_factor.errors.append("Two factor auth device failure")
            return False
        return True


class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        id="uname",
        validators=[
            DataRequired(message="Failure, Username is required."),
            Length(min=3, max=25),
        ],
    )
    password = PasswordField(
        "Password",
        id="pword",
        validators=[
            DataRequired(message="Failure, Password is required."),
            Length(min=4, max=128),
        ],
    )
    two_factor = StringField(
        "Two Factor Auth Device",
        id="2fa",
        validators=[
            DataRequired(message="Failure, Two Factor Auth device is required.")
        ],
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate_2fa(form, field):
        if len(field.data) > 16:
            raise ValidationError("Failure, invalid phone number.")
        try:
            input_number = phonenumbers.parse(field.data)
            if not phonenumbers.is_valid_number(input_number):
                raise ValidationError("Failure, invalid phone number.")
        except phonenumbers.NumberParseException:
            input_number = phonenumbers.parse(f"+1{field.data}")
            if not phonenumbers.is_valid_number(input_number):
                raise ValidationError("Failure, invalid phone number.")

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False

        db = get_db()
        if (
            db.execute(
                "SELECT id FROM user WHERE username = ?", (self.username.data,)
            ).fetchone()
            is not None
        ):
            self.username.errors.append(
                f"User {self.username.data} is already registered."
            )
            return False
        return True
