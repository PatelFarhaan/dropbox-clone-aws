from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, TextAreaField


class BlogPostForm(FlaskForm):

    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])
    submit = SubmitField("POST")