import os
from dotenv import load_dotenv


load_dotenv()


# App settins

API_KEY = os.environ.get("API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

# Session settings

SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"

# Database settings

SQLALCHEMY_DATABASE_URI = "sqlite:///tmdb.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Mail settings

MAIL_SERVER: "smtp.gmail.com"
MAIL_PORT: 465
MAIL_USE_TLS: False
MAIL_USE_SSL: True
MAIL_USERNAME: os.environ.get("EMAIL_USER")
MAIL_PASSWORD: os.environ.get("EMAIL_PASSWORD")
