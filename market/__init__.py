from flask import Flask
from flask_sqlalchemy  import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///database.db'
app.config['SECRET_KEY']='d3b0b5d250f8ff8ffb883a35'

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view= "login_page"
login_manager.login_message_category= "info"


app.app_context().push()

from market import routes











# @app.route('/about/<username>')

# def about_page(username):
#     return f"<h1>this page for{username}</h1>"


# app.run(host='0.0.0.0',port=5000)