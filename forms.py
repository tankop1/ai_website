from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, RadioField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length

class Login(FlaskForm):
    username = StringField('Username*', validators=[DataRequired()])
    password = PasswordField('Password*', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')

class Register(FlaskForm):
    first_name = StringField('First Name*', validators=[DataRequired()])
    last_name = StringField('Last Name*', validators=[DataRequired()])
    email = StringField('Email*', validators=[DataRequired(), Email()])
    username = StringField('Username*', validators=[DataRequired()])
    password = PasswordField('Password*', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password*', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

class ContactUs(FlaskForm):
    subject = StringField('Subject')
    message = TextAreaField('Message')
    submit = SubmitField('Send')

class MakeAI(FlaskForm):
    wake_word = StringField('Wake Word*', validators=[DataRequired()])
    types = [('Male', 'Male'), ('Female', 'Female')]
    voice = RadioField('Default Voice*', validators=[DataRequired()], choices=types)
    purchase = BooleanField('Allow Voice Purchasing')
    tracking = BooleanField('Allow Location Tracking')
    types2 = [('Windows', 'Windows'), ('MacOS', 'MacOS'), ('Linux', 'Linux')]
    os = RadioField('Operating System*', validators=[DataRequired()], choices=types2)
    files = BooleanField('Allow File Access')
    files2 = BooleanField('Allow Changing of Files')
    user_names = StringField('Names of Users*', validators=[DataRequired()])
    sos = StringField('SOS Command*', validators=[DataRequired()])
    commands = TextAreaField('Your Commands')
    submit = SubmitField('Checkout')

class PurchaseInfo(FlaskForm):
    card_number = StringField('Credit Card Number*', validators=[DataRequired()])
    cvv_code = StringField('CVV*', validators=[DataRequired()])
    expiration = StringField('Expiration Date*', validators=[DataRequired()])
    save_card = BooleanField('Save Card Information')
    submit = SubmitField('Place Order')