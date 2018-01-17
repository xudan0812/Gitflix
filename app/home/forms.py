# coding: utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp
from app.models import User
from sqlalchemy import or_


class RegisterForm(FlaskForm):
    """user register form"""
    username = StringField(
        label="Username",
        validators=[
            DataRequired("Enter a username")
        ],
        description="username",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "Enter a username",
            # "required": "required"
        }
    )
    email = StringField(
        label="Email",
        validators=[
            DataRequired("Enter an email"),
            Email("Invalid email format")
        ],
        description="email",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "Enter an email",
            # "required": "required"
        }
    )
    phone = StringField(
        label="Phone",
        validators=[
            DataRequired("Enter a phone number"),
            Regexp("[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]", message="Invalid phone number")
        ],
        description="phone",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "Enter a phone number",
            # "required": "required"
        }
    )
    pwd = PasswordField(
        label="Password",
        validators=[
            DataRequired("Enter a password")
        ],
        description="password",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "Enter a password",
            # "required": "required"
        }
    )
    confirm_pwd = PasswordField(
        label="Confirm Password",
        validators=[
            DataRequired("Enter the password again"),
            EqualTo('pwd', message="Don't match")
        ],
        description="confirm password",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "Enter the password again",
            # "required": "required"
        }
    )
    submit = SubmitField(
        "Submit",
        render_kw={
            "class": "btn btn-success btn-block btn-lg"
        }
    )

    def validate_username(self, field):
        username = field.data
        userCount = User.query.filter_by(name=username).count()
        if userCount == 1:
            raise ValidationError("Username already exists")

    def validate_phone(self, field):
        phone = field.data
        phoneCount = User.query.filter_by(phone=phone).count()
        if phoneCount == 1:
            raise ValidationError("Phone already exists")

    def validate_email(self, field):
        email = field.data
        emailCount = User.query.filter_by(email=email).count()
        if emailCount == 1:
            raise ValidationError("Email already exists")


class LoginForm(FlaskForm):
    """user login form"""
    account = StringField(
        label="Account",
        validators=[
            DataRequired("Username, email address or phone number")
        ],
        description="account",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "Enter your username, email address or phone number",
            # "required": "required"
        }
    )
    pwd = PasswordField(
        label="Password",
        validators=[
            DataRequired("Enter your password")
        ],
        description="password",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "Enter a password",
            # "required": "required"
        }
    )
    submit = SubmitField(
        "Submit",
        render_kw={
            "class": "btn btn-success btn-block btn-lg"
        }
    )

    def validate_account(self, field):
        account = field.data
        userCount = User.query.filter(or_(User.name==account, User.email==account, User.phone==account)).count()
        if userCount == 0:
            raise ValidationError("User does not exist")


class UserDetailForm(FlaskForm):
    username = StringField(
        label="Username",
        validators=[
            DataRequired("Enter a new username")
        ],
        description="username",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "Enter a new username",
            # "required": "required"
        }
    )
    email = StringField(
        label="Email",
        validators=[
            DataRequired("Enter a new email"),
            Email("Invalid email format")
        ],
        description="email",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "Enter a new email",
            # "required": "required"
        }
    )
    phone = StringField(
        label="Phone",
        validators=[
            DataRequired("Enter a new phone number"),
            Regexp("[0-9][0-9][0-9]-[0-9][0-9][0-9]-[0-9][0-9][0-9][0-9]", message="Invalid phone number")
        ],
        description="phone",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "Enter a new phone number",
            # "required": "required"
        }
    )
    avatar = FileField(
        label="Avatar",
        validators=[
            DataRequired("Upload a new avatar")
        ],
        description="Avatar"
    )
    info = TextAreaField(
        label="Info",
        validators=[
            DataRequired("Enter a new info")
        ],
        description="Info",
        render_kw={
            "class": "form-control",
            "rows": 10
            # "id": "input_info"
        }
    )
    submit = SubmitField(
        "Submit",
        render_kw={
            "class": "btn btn-success"
        }
    )


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="Old Password",
        validators=[
            DataRequired("Enter your old password")
        ],
        description="old password",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "Enter your old password",
            # "required": "required"
        }
    )
    new_pwd = PasswordField(
        label="New Password",
        validators=[
            DataRequired("Enter your new password")
        ],
        description="new password",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "Enter your new password",
            # "required": "required"
        }
    )
    submit = SubmitField(
        "Submit",
        render_kw={
            "class": "btn btn-success"
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["user"]
        user = User.query.filter_by(
            name=name
        ).first()
        if not user.check_pwd(pwd):
            raise ValidationError("Old password is wrong")


class CommentForm(FlaskForm):
    content = TextAreaField(
        label="Comment Content",
        validators=[
            DataRequired("Enter a comment")
        ],
        description="comment content",
        render_kw={
            "id": "input_content"
        }
    )
    submit = SubmitField(
        "Submit",
        render_kw={
            "class": "btn btn-success",
            "id": "btn-sub"
        }
    )
