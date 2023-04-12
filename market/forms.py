from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Length,DataRequired,Email,EqualTo,ValidationError
from market.models import User

class Registerform(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try a different username')

    def validate_email_address(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email Address already exists! Please try a different email address')


    username=StringField(label='UserName',validators=[ Length(min=2,max=30),DataRequired()])
    email=StringField(label='Email',validators=[Email(),DataRequired()])
    password1=PasswordField(label='password',validators=[ Length(min=6),DataRequired()])
    password2=PasswordField(label='Confirm password',validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label='Create Account')


class loginform(FlaskForm):
    username=StringField(label='UserName',validators=[DataRequired()])
    password=PasswordField(label='Password',validators=[DataRequired()])
    submit=SubmitField(label='Sign in')




class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')


