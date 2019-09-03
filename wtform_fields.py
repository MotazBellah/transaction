from flask_wtf import FlaskForm
from models import User
from passlib.hash import pbkdf2_sha256
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError

# custom validator for registeration form, to check if email dublicate
def email_exists(form, field):
    user_object = User.query.filter_by(email=field.data).first()
    if user_object:
        raise ValidationError("This email is aleardy exists")


def invalid_credentials(form, field):
    """ Password checker """

    email_entered = form.email.data
    password_entered = field.data

    # Check if credentials is valid
    user_object = User.query.filter_by(email=email_entered).first()
    if user_object is None:
        raise ValidationError("Email or password is incorrect")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Email or password is incorrect")


class RegistartionForm(FlaskForm):
    """ Registartion Form """

    username = StringField('username_lable',
                            validators=[InputRequired(message="Username Required"),
                                        Length(min=4, max=25, message="Username must be between 4 and 25 charachters")])
    email = StringField('email_lable',
                        validators=[InputRequired(message="Email Required"), Email(message="This field requires a valid email address"), email_exists])
    description = TextAreaField('description_lable',
                        validators=[Length(max=1000)])
    password = PasswordField('password_lable',
                             validators=[InputRequired(message="Password Required"),
                                        Length(min=4, max=25, message="Password must be between 4 and 25 charachters")])
    confirm_pswd = PasswordField('confirm_pswd_lable',
                                 validators=[InputRequired(message="Password confirmation Required"),
                                            EqualTo('password', message="Password must match!")])

    submit_button = SubmitField("Create")


class LoginForm(FlaskForm):
    """ Login Form """

    email = StringField('email_lable',
                        validators=[InputRequired(message="Email Required"), Email(message="This field requires a valid email address")])
    password = PasswordField('password_lable',
                             validators=[InputRequired(message="Password Required"), invalid_credentials])
    submit_button = SubmitField("Login")
