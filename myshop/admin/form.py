from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,Email,DataRequired,EqualTo,ValidationError
from  myshop.customer.models import Customer

class RegisterForm(FlaskForm):
 name=StringField('Name',
                  validators=[DataRequired(),Length(min=2,max=20)])
 username=StringField('Username',
                  validators=[DataRequired(),Length(min=2,max=20)])
 email=StringField('Email Address',
                   validators=[DataRequired(),Email()])
 password=PasswordField('New Password', 
                   validators=[DataRequired()])
 comfirm_password=PasswordField('Repeat Password',
                   validators=[DataRequired(),EqualTo('password')])
 picture=FileField('Photo',validators=[FileAllowed(['jpg','png'])])
 submit=SubmitField('Register')

 def validate_username(self,username):
     user=Customer.query.filter_by(username=username.data).first()
     if user:
         raise ValidationError('That username was taken.')

 def validate_email(self,email):
     user=Customer.query.filter_by(email=email.data).first()
     if user:
         raise ValidationError('That email was taken.')

class LoginForm(FlaskForm):
 email=StringField('Email Address',
                   validators=[DataRequired(),Email()])
 password=PasswordField('Password', 
                   validators=[DataRequired()])
 submit=SubmitField('Sign In')

 
