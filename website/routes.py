from website import app
from flask import render_template, redirect, url_for, flash
from website.forms import SignupForm, LoginForm, ChangePasswordForm
from website.models import User, Item
from website import db
from flask_login import login_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
@login_required
def market_page():
    # Assuming Item is defined somewhere in your code
    items = Item.query.all()
    return render_template('market.html', items=items)

from flask import render_template, redirect, url_for, flash
from flask_login import login_user, current_user

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()

        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Welcome, {attempted_user.username}!', category='success')

            # Check if the logged-in user has id equal to 1
            if current_user.is_authenticated and current_user.id == 1:
                return render_template('admin_dashboard.html')
            else:
                return redirect(url_for('home_page'))

    flash('No match! Please try again', category='danger')
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    form = SignupForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Yay! Account Created, you are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('home_page'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error with creating a user: {err_msg}', category='danger')

    return render_template('signup.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/profile/<int:user_id>', methods=['GET'])
@login_required
def profile_get(user_id):
    user = User.query.get_or_404(user_id)
    form = ChangePasswordForm()  # Create an instance of your ChangePasswordForm
    return render_template('profile.html', user=user, form=form)

@app.route('/profile/<int:user_id>', methods=['POST'])
@login_required
def profile_post(user_id):
    user = User.query.get_or_404(user_id)
    form = ChangePasswordForm()  # Create an instance of your ChangePasswordForm

    if form.validate_on_submit():
        # Handle form submission and change password logic here
        flash('Password changed successfully!', 'success')

    return render_template('profile.html', user=user, form=form)



