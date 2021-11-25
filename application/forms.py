from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import User


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=8)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):

        username_taken = User.query.filter_by(
            username=username.data.lower()).first()

        if username_taken:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

    def validate_email(self, email):

        email_taken = User.query.filter_by(
            email=email.data.lower()).first()

        if email_taken:
            raise ValidationError(
                'An account already exists using this email. Please choose a different one.')


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class UpdateProfileForm(FlaskForm):

    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Save changes')

    def validate_username(self, username):

        if username.data != current_user.username:

            username_taken = User.query.filter_by(
                username=username.data.lower()).first()

            if username_taken:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):

        if email.data != current_user.email:

            email_taken = User.query.filter_by(
                email=email.data.lower()).first()

            if email_taken:
                raise ValidationError(
                    'An account already exists using this email. Please choose a different one.')


class PostForm(FlaskForm):

    content = TextAreaField('Content', validators=[
                            DataRequired(), Length(max=300)])
    submit = SubmitField('Post')
