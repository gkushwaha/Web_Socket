from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


#validation Form for resister Page
class ResistrationForm(FlaskForm):
	username =StringField('Name', validators=[DataRequired(),
							 Length(min=2, max=50)]) 
	email= StringField('Email', validators=[DataRequired(),
							 Email()])
	password = PasswordField('Password', validators=[DataRequired()])

	conform_password = PasswordField('Conform Password', 
									validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

#validation form for loginpage
class LoginForm(FlaskForm):
	email= StringField('Email', validators=[DataRequired(),
							 Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


