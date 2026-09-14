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


class UpdateProfileForm(FlaskForm):

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

    submit = SubmitField("Save Profile Changes")


class ChangePasswordForm(FlaskForm):

    current_password = PasswordField(
        "Current Password",
        validators=[
            DataRequired(
                message="Enter your current password."
            )
        ]
    )

    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            Length(
                min=10,
                max=128,
                message="New password must be at least 10 characters."
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

    confirm_new_password = PasswordField(
        "Confirm New Password",
        validators=[
            DataRequired(),
            EqualTo(
                "new_password",
                message="Passwords do not match."
            )
        ]
    )

    submit = SubmitField("Update Password")


class DeleteAccountForm(FlaskForm):

    password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(
                message="Enter your password to authorize account deletion."
            )
        ]
    )

    confirm_phrase = StringField(
        "Type DELETE to confirm",
        validators=[
            DataRequired(
                message="Please type DELETE in capital letters."
            )
        ]
    )

    submit = SubmitField("Permanently Delete My Account")