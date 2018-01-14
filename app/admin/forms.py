# coding: utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin, Tag

tags = Tag.query.all()


class LoginForm(FlaskForm):
    """admin login form"""
    username = StringField(
        label="username",
        validators=[
            DataRequired("Enter a username")
        ],
        description="username",
        render_kw={
            "class": "form-control",
            "placeholder": "Enter a username",
            "required": "required"
        }
    )
    pwd = PasswordField(
        label="password",
        validators=[
            DataRequired("Enter a password")
        ],
        description="password",
        render_kw={
            "class": "form-control",
            "placeholder": "Enter a password",
            "required": "required"
        }
    )
    submit = SubmitField(
        "submit",
        render_kw={
            "class": "btn btn-primary btn-block btn-flat"
        }
    )

    def validate_username(self, field):
        username = field.data
        adminCount = Admin.query.filter_by(name=username).count()
        if adminCount == 0:
            raise ValidationError("username does not exist")


class TagForm(FlaskForm):
    """tag form"""
    tagName = StringField(
        label="Tag Name",
        validators=[
            DataRequired("Enter a tag name")
        ],
        description="Tag Name",
        render_kw={
            "class": "form_control",
            "id": "input_name",
            "placeholder": "Enter a tag name"
        }
    )
    submit = SubmitField(
        "Submit",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class MovieForm(FlaskForm):
    title = StringField(
        label="Title",
        validators=[
            DataRequired("Please type in a title")
        ],
        description="Title",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "Please enter a title"
        }
    )
    url = FileField(
        label="File",
        validators=[
            DataRequired("Please upload a file")
        ],
        description="File"
    )
    info = TextAreaField(
        label="Info",
        validators=[
            DataRequired("Please enter an info")
        ],
        description="Info",
        render_kw={
            "class": "form-control",
            "rows": 10,
            "id": "input_info"
        }
    )
    logo = FileField(
        label="Logo",
        validators=[
            DataRequired("Please upload a logo")
        ],
        description="Logo"
    )
    star = SelectField(
        label="Rating",
        coerce=int,
        choices=[(1, "1 star"),(2, "2 starts"),(3, "3 starts"),(4, "4 starts"),(5, "5 starts")],
        validators=[
            DataRequired("Please provide a rating")
        ],
        description="Rating",
        render_kw={
            "class": "form-control"
        }
    )
    tag = SelectField(
        label="Tag",
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        validators=[
            DataRequired("Please provide a tag")
        ],
        description="Tag",
        render_kw={
            "class": "form-control"
        }
    )
    area = StringField(
        label="Area",
        validators=[
            DataRequired("Please type in an area")
        ],
        description="Area",
        render_kw={
            "class": "form-control",
            "placeholder": "Please provide an area"
        }
    )
    length = StringField(
        label="Length",
        validators=[
            DataRequired("Please type in a length")
        ],
        description="Length",
        render_kw={
            "class": "form-control",
            "placeholder": "Please provide a length"
        }
    )
    release_time = StringField(
        label="Release Time",
        validators=[
            DataRequired("Please select a release time")
        ],
        description="Release Time",
        render_kw={
            "class": "form-control",
            "placeholder": "Please select a release time",
            "id": "input_release_time"
        }
    )
    submit = SubmitField(
        "Submit",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class PreviewForm(FlaskForm):
    title = StringField(
        label="Title",
        validators=[
            DataRequired("Please type in a title")
        ],
        description="Title",
        render_kw={
            "class": "form-control",
            "id": "input_title",
            "placeholder": "Please enter a title"
        }
    )
    logo = FileField(
        label="Logo",
        validators=[
            DataRequired("Please upload a logo")
        ],
        description="Logo"
    )
    submit = SubmitField(
        "Submit",
        render_kw={
            "class": "btn btn-primary"
        }
    )


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="Old Password",
        validators=[
            DataRequired("Enter the old password")
        ],
        description="Old Password",
        render_kw={
            "class": "form_control",
            "placeholder": "Enter the old password"
        }
    )
    new_pwd = PasswordField(
        label="New Password",
        validators=[
            DataRequired("Enter a new password")
        ],
        description="New Password",
        render_kw={
            "class": "form_control",
            "placeholder": "Enter a new password"
        }
    )
    submit = SubmitField(
        "Submit",
        render_kw={
            "class": "btn btn-primary"
        }
    )

    def validate_old_pwd(self, field):
        from flask import session
        pwd = field.data
        name = session["admin"]
        admin = Admin.query.filter_by(
            name=name
        ).first()
        if not admin.check_pwd(pwd):
            raise ValidationError("Old password is wrong")


class AuthForm(FlaskForm):
    name = StringField(
        label="Auth Name",
        validators=[
            DataRequired("Enter an auth name")
        ],
        description="Auth Name",
        render_kw={
            "class": "form_control",
            "placeholder": "Enter an auth name"
        }
    )
    url = StringField(
        label="Auth Address",
        validators=[
            DataRequired("Enter an auth address")
        ],
        description="Auth Address",
        render_kw={
            "class": "form_control",
            "placeholder": "Enter an auth address"
        }
    )
    submit = SubmitField(
        "Submit",
        render_kw={
            "class": "btn btn-primary"
        }
    )