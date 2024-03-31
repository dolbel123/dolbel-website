from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField,IntegerField,TextAreaField, FileField, SelectField, FloatField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError, NumberRange
from website.models import User
from flask_wtf.file import FileRequired

class SignupForm(FlaskForm):
    username = StringField(validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(validators=[Email(), DataRequired()])
    password = PasswordField(validators=[Length(min=6), DataRequired()])
    repeat_password = PasswordField(validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField()

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one.')

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email address is already registered. Please use a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[ DataRequired()]) 
    password = PasswordField(validators=[ DataRequired()])
    submit = SubmitField()


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')


class ShopItemsForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=30)])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    barcode = StringField('Barcode', validators=[DataRequired(), Length(min=13, max=13)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(max=1324)])
    product_detail = TextAreaField('Product Detail', validators=[DataRequired(), Length(max=1000)])
    in_stock = IntegerField('In Stock', validators=[DataRequired(), NumberRange(min=0)])
    product_picture = FileField('product picture', validators=[FileRequired()])
    submit = SubmitField('Add Product')


class OrderForm(FlaskForm):
    status = SelectField('Order Status', choices=[('Pending','Pending'),('Accepted', 'Accepted'),('Out for delivery','Out for delvery'),('Delivered','Delivered'),('Cancelled','Cancelled')])

    update = SubmitField('Update Status')



class AuctionForm(FlaskForm):
    # Define the fields for adding or updating auction items
    product_picture = FileField('product picture', validators=[FileRequired()])
    item_name = StringField('Item Name', validators=[DataRequired(), Length(min=1, max=100)])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_time = StringField('Start Time', id='datepick', validators=[DataRequired()])
    end_time = StringField('End Time', id='datepick', validators=[DataRequired()])
    current_bid = FloatField('Current Bid', validators=[NumberRange(min=0)])
    item_id = IntegerField('Item ID', validators=[DataRequired()])
    submit = SubmitField('List Item')
    def validate_end(self, field):
        if field.data <= self.start_time.data:
            raise ValidationError(
                "Error!: Please enter a later date than the start date.")

class ReviewForm(FlaskForm):
    # Define the fields for adding or updating reviews
    review = TextAreaField(validators=[DataRequired(), Length(min=5, max=400, message='Comment is too long or too short')])

    submit = SubmitField('Write Review')
    product_picture = StringField('Product Picture URL', validators=[DataRequired(), Length(max=1000)])
   

class BidForm(FlaskForm):
    # Define the fields for adding or updating bids
    bid_amount = FloatField('Bid Amount', validators=[DataRequired(), NumberRange(min=1)])
    place = SubmitField('Place Bids')