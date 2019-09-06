from flask_wtf import FlaskForm
from models import User, Currency
from passlib.hash import pbkdf2_sha256
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, IntegerField, Optional
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

# custom validator for registeration form, to check if email dublicate
def bitcoin_id_exists(form, field):
    currency_object = Currency.query.filter_by(bitcoin_id=field.data).first()
    if currency_object:
        raise ValidationError("This bitcoin id is aleardy exists")

# custom validator for registeration form, to check if email dublicate
def ethereum_id_exists(form, field):
    currency_object = Currency.query.filter_by(ethereum_id=field.data).first()
    if currency_object:
        raise ValidationError("This ethereum id is aleardy exists")


# custom validator for registeration form, to check if email dublicate
def ethereum_id_exists(form, field):
    currency_object = Currency.query.filter_by(ethereum_id=field.data).first()
    if currency_object:
        raise ValidationError("This ethereum id is aleardy exists")

# custom validator for registeration form, to check if email dublicate
def balance_not_number(form, field):
    balance_number = field.data
    if balance_number:
        try:
            int(balance_number)
        except ValueError:
            raise ValidationError("The balance should be number")


# # custom validator for registeration form, to check if email dublicate
# def target_user_exsits(form, field):
#     user_object = User.query.filter_by(id=field.data).first()
#     if not user_object:
#         raise ValidationError("This user is not exists, Please check the ID")


def target_user_account(form, field):
    target_user = User.query.filter_by(id=field.data).first()
    if target_user:
        currency_account = Currency.query.filter_by(user_id=target_user.id).first()
    else:
        raise ValidationError("This user is not exists, Please check the ID")
    if not currency_account:
        raise ValidationError("This user has no currency account!")


def currency_Type_exsits(form, field):
    currency_type = field.data
    if currency_type.lower() not in  ['bitcoin', 'ethereum']:
        raise ValidationError("The currency type should be bitcoin or ethereum")



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

###### Check this form ####
class CurrencyForm(FlaskForm):
    """ Currency Form """

    bitcoin_id = IntegerField('bitcoin_id', validators=[InputRequired(message="Bitcoin Wallet Id is required"), bitcoin_id_exists])
    bitcoin_balance = FloatField('bitcoin_balance', validators=[InputRequired(message="Bitcoin Wallet balance is required"), balance_not_number])
    ethereum_id = IntegerField('ethereum_id',
                                 validators=[InputRequired(message="Ethereum Wallet Id is required"), ethereum_id_exists])
    ethereum_balance = FloatField('ethereum_balance',
                             validators=[InputRequired(message="Ethereum Wallet balance is required"), balance_not_number])
    max_amount = FloatField('max_amount', validators=[InputRequired(message="Max amount that is allowed per transaction is required")])


class EditCurrencyForm(FlaskForm):
    """ Edit Currency Form """

    bitcoin_id = IntegerField('bitcoin_id', validators=[ Optional(), bitcoin_id_exists])
    bitcoin_balance = FloatField('bitcoin_balance', validators=[ Optional(), balance_not_number])
    ethereum_id = IntegerField('ethereum_id', validators=[Optional(), ethereum_id_exists])
    ethereum_balance = FloatField('ethereum_balance', validators=[Optional(), balance_not_number])
    max_amount = FloatField('max_amount', [validators.Optional()])



###### Check this form ####
class TransactionForm(FlaskForm):
    """ Transaction Form """

    currency_amount = FloatField('currency_amount', validators=[InputRequired(message="currency amount is required")])
    currency_Type = StringField('currency_Type', validators=[InputRequired(message="currency type is required"), currency_Type_exsits])
    target_user = IntegerField('target_user',
                                 validators=[InputRequired(message="target user Id is required"), target_user_account])
