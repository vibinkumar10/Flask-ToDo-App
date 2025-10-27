from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email

class Login_form(FlaskForm):
    email = StringField("Email :",validators=[DataRequired(),Email()])
    password = PasswordField("Password :",validators=[DataRequired(),Length(min=5,max=15)])
    submit = SubmitField("Login")

class Register_form(FlaskForm):
    name = StringField("Name :",validators=[DataRequired(),Length(max=50)])
    email = StringField("Email :",validators=[DataRequired(),Email()])
    password = PasswordField("Password :",validators=[DataRequired(),Length(min=5,max=15)])
    submit = SubmitField("Register")

class Task_form(FlaskForm):
    task = StringField("Task :",validators=[DataRequired(),Length(max=20)])
    submit = SubmitField("Add")