from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'e68257145e89a237de02e9cf'
db = SQLAlchemy(app)
hkjkkjkj
bcrypt= Bcrypt(app)


 
login_manager = LoginManager(app)
login_manager.login_view = "login_page"

from website import routes
from .admin import admin
from .views import views

app.register_blueprint(admin, url_prefix='/')
app.register_blueprint(views, url_prefix='/')

@app.errorhandler(404)
def not_found_error(error):
 return render_template('404.html'), 404


app.app_context().push() 
   
