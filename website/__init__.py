# imports
from logging import log
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager, login_manager

# initialise database
db = SQLAlchemy()
DB_NAME = "database.db"

# create app
def create_app():
    # initialize the app
    app = Flask(__name__)

    # set decryption
    app.config["SECRET_KEY"] = "development"

    # connect database
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    # import routes
    from .views import views
    from .auth import auth

    app.register_blueprint(views, urL_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")

    # check database
    from .models import User, Note
    create_database(app)

    # start login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# create database
def create_database(app):
    if not path.exists(f"website/{DB_NAME}"):
        db.create_all(app = app)
        print("Database created")