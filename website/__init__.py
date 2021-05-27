from flask import Flask

def create_app():
    # create the app
    app = Flask(__name__)

    # set decription
    app.config["SECRET_KEY"] = "development"

    # import routes
    from .views import views
    from .auth import auth

    app.register_blueprint(views, urL_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")
    return app