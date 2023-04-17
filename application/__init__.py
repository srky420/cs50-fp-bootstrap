from flask import Flask
from flask_session import Session
from .models import *


def create_app():
    # App config
    app = Flask(__name__)
    app.secret_key = "c1a199f5305f80a0363da7df089151ccae0e2ac3a2f1f062fa8bed7b7db3c7af"

    # Session config
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)

    # SQLAlchemy config
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///allmovie.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    
    return app