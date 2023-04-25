from functools import wraps
from flask import redirect, session, flash
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired
import os, re
from dotenv import load_dotenv


load_dotenv()


s = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            flash("Login required!", "error")
            return redirect("/login")

        return f(*args, **kwargs)
    return decorated_function


# Check for valid email
def valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if (re.fullmatch(regex, email)):
        return True
    
    return False


# Create confirmation token
def create_email_token(email):
    token = s.dumps(email, salt=os.getenv("SECRET_SALT"))
    return token


# Load confirmation token
def get_confirmation_email(token):
    try:
        email = s.loads(token, salt=os.getenv("SECRET_SALT"))
        return email
    except (BadTimeSignature, SignatureExpired) as e:
        return e