from flask import Flask
from .extensions import db, session
from .views import views
from .auth import auth


def create_app(config_file='settings.py'):

    # App config
    app = Flask(__name__)
    app.config.from_pyfile(config_file)

    # Session config
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    # SQLAlchemy config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///allmovie.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Register blueprints
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Initialize extentions
    db.init_app(app)
    session.init_app(app)

    return app
