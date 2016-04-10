from flask.ext.wtf import Form
from wtforms import ValidationError, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from app.models import User

banned_usernames = [
    'edit-profile',
]


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    password = PasswordField('Pasword', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Log In')


class RegistrationForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1,64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1,64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0,
                                                          'Usernames may only contain letters, \
                                                          numbers or underscores.')])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     EqualTo('password2', message='Passwords do not match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() or field.data in banned_usernames:
            raise ValidationError('Username already in use.')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[DataRequired()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Reset Password')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class ChangeEmailForm(Form):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')