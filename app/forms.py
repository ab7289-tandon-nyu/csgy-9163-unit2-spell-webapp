from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField

# import phonenumbers
from wtforms.validators import DataRequired, Length

from app.models import User

# Flask-WTF form definitions. These aide in form validation


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()], id="uname")
    # todo restrict special characters except for '_'
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

        self.user = User.query.filter_by(username=self.username.data).first()

        if not self.user or not self.user.check_password(self.password.data):
            self.username.errors.append("faiture, Incorrect username or password")
            return False

        if not self.user.check_two_factor(self.two_factor.data):
            self.two_factor.errors.append("failure, Two-factor auth device failure")
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
            DataRequired(message="Failure, Two Factor Auth device is required."),
            Length(min=11, max=11),
        ],
    )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    # def validate_two_factor(form, field):
    #     """ handy function to validate that the value input in the Two Factor
    #     field is a valid US phone Number """
    #     try:
    #         input_number = phonenumbers.parse(field.data, region="US")
    #         if not phonenumbers.is_possible_number(input_number):
    #             raise ValidationError("Failure, invalid phone number.")
    #     except phonenumbers.NumberParseException:
    #         # input_number = phonenumbers.parse("+1"+field.data)
    #         # if not phonenumbers.is_valid_number(input_number):
    #         raise ValidationError("Failure, invalid phone number.")

    def validate(self):
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False

        # check to make sure that the specified username hasn't already been registered
        if User.query.filter_by(username=self.username.data).first() is not None:
            self.username.errors.append(
                f"failure, User {self.username.data} is already registered."
            )
            return False
        return True


class SpellForm(FlaskForm):

    inputtext = TextAreaField("Please enter your text", validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(SpellForm, self).__init__(*args, **kwargs)


class HistoryForm(FlaskForm):

    userquery = StringField(
        "Enter the username",
        id="userquery",
        validators=[DataRequired(), Length(min=3, max=25)],
    )

    def __init__(self, *args, **kwargs):
        super(HistoryForm, self).__init__(*args, **kwargs)


class AuthHistoryForm(FlaskForm):
    """form to retrieve the auth history for a user, would just have reused the HistoryForm
    except for the requirement that the input field id be 'userid' instead of 'userquery'"""

    userid = StringField(
        "Enter the username",
        id="userid",
        validators=[DataRequired(), Length(min=3, max=25)],
    )

    def __init__(self, *args, **kwargs):
        super(AuthHistoryForm, self).__init__(*args, **kwargs)
