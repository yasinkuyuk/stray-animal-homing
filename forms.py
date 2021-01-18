from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField, FloatField, SelectField, FileField
from wtforms.validators import EqualTo, Length, DataRequired,NumberRange
import hashlib

class RegistationForm(FlaskForm):
    username = StringField("*Username", validators=[DataRequired(),Length(3,15)])
    city = StringField("City")
    district = StringField("District")
    userType = StringField("Ad Owner/Ad Looker")
    phoneNumber = StringField("XXX XXX XXXX (without 0)")
    password = PasswordField("*Password" , validators=[DataRequired()])
    confirmPassword = PasswordField("*Confirm Password" , validators=[DataRequired(),EqualTo("password")])
    submit = SubmitField("Sign Up")
    
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(),Length(3,15)])
    password = PasswordField("Password" , validators=[DataRequired()])
    submit = SubmitField("Sign In")

class updateUserInformation(FlaskForm):
    city = StringField("City")
    district = StringField("District")
    userType = StringField("Ad Owner/Ad Looker")
    phoneNumber = StringField("XXX XXX XXXX (without 0)")
    password = PasswordField("Change Password")
    confirmPassword = PasswordField("Confirm Changed Password", validators=[EqualTo("password")])
    submit = SubmitField("Save Changes")

class AdvertisementForm(FlaskForm):
    age = IntegerField("Age of Animal")
    breed = StringField("Breed of Animal",validators=[DataRequired()])
    health_status = StringField("Health Status")
    submit = SubmitField("Create an Advertisement")

class VoteForm(FlaskForm):
    username = SelectField("Enter the username that you want to vote.", validators=[DataRequired()],choices=[])
    vote = SelectField("Enter between 0-10",validators=[DataRequired()], choices=[1,2,3,4,5,6,7,8,9,10])
    submit = SubmitField("Vote")

class DonationForm(FlaskForm):
    amount = FloatField("Amount of Donation", validators=[DataRequired()])
    submit = SubmitField("Donate")

class SearchAdvertisementForm(FlaskForm):
    breed = StringField("Search By Breed", validators=[DataRequired()])
    submit = SubmitField("Search")

def hashPassword(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

class filefield(FlaskForm):
    filef = FileField("file upload")
    submit = SubmitField("upload")

class Homing(FlaskForm):
    ad_id = SelectField("Select Advertisement Id",validators=[DataRequired()],choices=[])
    username = SelectField("Select Username",validators=[DataRequired()],choices=[])
    submit = SubmitField("Remove")



