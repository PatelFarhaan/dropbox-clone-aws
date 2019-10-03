from flask_wtf import FlaskForm
from project.models import Users
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Email
from wtforms import StringField, SubmitField, ValidationError


class UpdateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def check_email(self,field):
        if Users.query.filter_by(email=field.email).first():
            raise ValidationError('Your Email has Already been taken')

    def check_usename(self,field):
        if Users.query.filter_by(username=field.username).first():
            raise ValidationError('Sorry, that Username has already been taken!!!')