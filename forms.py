from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    EqualTo,
    Regexp
)


class RegistrationForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=30),
            Regexp(
                r"^[A-Za-z0-9_-]+$",
                message=(
                    "Username can contain only letters, "
                    "numbers, underscores and hyphens."
                )
            )
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Length(max=120),
            Regexp(
                r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
                message="Enter a valid email address."
            )
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(
                min=10,
                max=128,
                message="Password must be at least 10 characters."
            ),
            Regexp(
                r"^(?=.*[A-Za-z])(?=.*\d).+$",
                message=(
                    "Password must contain at least "
                    "one letter and one number."
                )
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords do not match."
            )
        ]
    )

    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(max=30)
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(max=128)
        ]
    )

    submit = SubmitField("Login")