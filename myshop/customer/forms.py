from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Length,EqualTo,Email,ValidationError
from myshop.customer.models import Customer

class CustomerRegister(FlaskForm):
    name=StringField('Name',
                   validators=[DataRequired(),Length(min=2,max=30)])
    username=StringField('Username',
                   validators=[DataRequired(),Length(min=3,max=40)])
    email=StringField('Email',
                   validators=[DataRequired(),Email()])
    password=PasswordField('Password',
                    validators=[DataRequired()])
    comfirm_password=PasswordField('Comfirm Password',
                    validators=[DataRequired(),EqualTo('password')])
    country=StringField('country',validators=[DataRequired()])
    state=StringField('State',validators=[DataRequired()])
    city=StringField('city',validators=[DataRequired()])
    contact=StringField('Contact',validators=[DataRequired()])
    address=StringField('Address',validators=[DataRequired()])
    zip_code=StringField('Zip Code',validators=[DataRequired()])
    profile=FileField('Profile',
                    validators=[FileAllowed(['png','jpg','jpeg','gif'])])
    submit=SubmitField('Sign Up')

    def validate_username(self,username):
        customer=Customer.query.filter_by(username=username.data).first()
        if customer:
            raise ValidationError('That username is in use! Please choose a different one.')

    def validate_email(self,email):
        customer=Customer.query.filter_by(email=email.data).first()
        if customer:
            raise ValidationError('That email is in use! Please choose a different one.')

class CustomerLogin(FlaskForm):
 email=StringField('Email Address',
                   validators=[DataRequired(),Email()])
 password=PasswordField('Password', 
                   validators=[DataRequired()])
 submit=SubmitField('Sign In')



