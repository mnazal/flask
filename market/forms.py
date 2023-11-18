from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

class RegisterForm(FlaskForm):

    def validate_username(self, username_check):
        user=User.query.filter_by(username=username_check.data).first()
        if user:
            raise ValidationError('User Already exists')
    def validate_email(self, email_check):
        email=User.query.filter_by(email=email_check.data) .first()
        if email:
            raise ValidationError('User with this email     Already exists')

    username = StringField(label='Username : ',validators=[Length(max=30,min=2),DataRequired()])
    email= StringField(label='Email : ',validators=[Email(),DataRequired()])
    password1= PasswordField(label='Password : ',validators=[Length(min=6),DataRequired()])
    password2=PasswordField(label='Confirm Password : ',validators=[EqualTo('password1'),DataRequired()])
    submit=SubmitField(label='Create Account')



class LoginForm(FlaskForm):
    username = StringField(label='Username : ',validators=[DataRequired()])
    password = PasswordField(label='Password : ',validators=[DataRequired()])
    submit=SubmitField(label='Create Account')


class PurchaseItemForm(FlaskForm):
     submit=SubmitField(label='Purchase')
class SellItemForm(FlaskForm):
     submit=SubmitField(label='Sell')
