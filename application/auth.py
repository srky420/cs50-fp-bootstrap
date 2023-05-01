from flask import Blueprint, request, redirect, render_template, flash, url_for, session, Markup
from .models import Users
from werkzeug.security import check_password_hash, generate_password_hash
from .extensions import db
from .utils import valid_email, send_email, create_email_token, parse_email_token, login_required
from dotenv import load_dotenv


load_dotenv()

auth = Blueprint("auth", __name__)


# LOGIN ROUTE
@auth.route("/login", methods=["GET", "POST"])
def login():
    # Check if already logged in
    if session.get("user_id") is not None:
        flash("Already logged in!", "error")
        return redirect("/")
    
    # POST
    if request.method == "POST":
        # Clear session
        session.clear()

        email = request.form.get("email")
        password = request.form.get("password")

        # Check for input
        if not email or not password:
            flash("Please provide all inputs!", "error")
            return redirect(url_for("auth.login"))
        elif not valid_email(email):
            flash("Invalid email!", "error")
            return redirect(url_for("auth.login"))
        
        # Check if user exists
        user = Users.query.filter_by(email=email).first()

        # Check if account is activated
        if user and not user.is_activated:
            # Send confirmation email
            token = create_email_token(email)
            link = url_for("auth.confirm_email", token=token, _external=True)
            html = render_template("confirmation-email.html", link=link)
            send_email("TMDb: Confirm Email", email, html)

            flash(message=Markup(f"Account not activated, an email has been sent to '{email}'"), category="neutral")
            return redirect(url_for("auth.login"))
        
        if not user or not check_password_hash(user.password, password):
            flash("Invalid email or password!", "error")
            return redirect(url_for("auth.login"))

        # Set session var
        session["user_id"] = user.id

        flash("Logged in!", "success")
        return redirect("/")

    # GET
    return render_template("login.html")


# LOGOUT ROUTE
@auth.route("/logout")
def logout():
    # Check if already logged in
    if session.get("user_id") is not None:

        # Clear session
        session.clear()
        flash("Logged out!", "neutral")

    return redirect("/")


# REGISTER ROUTE
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    # Check if already logged in
    if session.get("user_id"):
        flash("Already logged in!", "error")
        return redirect("/")

    # POST
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check input
        if not username or not password or not confirmation or not email:
            flash("Please provide all inputs!", "error")
            return redirect(url_for("auth.signup"))
        elif password != confirmation:
            flash("Passwords don't match!", "error")
            return redirect(url_for("auth.signup"))
        elif not valid_email(email):
            flash("Invalid email!", "error")
            return redirect(url_for("auth.signup"))

        # Check if user already exists
        user = Users.query.filter_by(email=email).first()

        if user:
            flash("Account already exists!", "error")
            return redirect(url_for("auth.signup"))

        # Create a user
        user = Users(email, username, generate_password_hash(password))

        # Add user to db
        db.session.add(user)
        db.session.commit()

        # Send confirmation email
        token = create_email_token(email)
        link = url_for("auth.confirm_email", token=token, _external=True)
        html = render_template("confirmation-email.html", link=link)

        send_email("TMDb: Confirm Email", email, html)

        flash(message=Markup(f"Account confirmation link has been sent to {email}"), category="success")
        return redirect("/login")

    # GET
    return render_template("signup.html")


# CONFIRM EMAIL ROUTE
@auth.route("/confirm-email/<token>")
def confirm_email(token):
    # Check if already logged in
    if session.get("user_id") is not None:
        flash("Already logged in!", "error")
        return redirect("/")
    
    try:
        # Decode token
        email = parse_email_token(token, 5400)
        
        # Verify user
        user = Users.query.filter_by(email=email).first()
        if not user or user.is_activated:
            flash("Error while verifying account!", "error")
            return redirect("/login")
        
        # Activate user
        user.is_activated = True
        db.session.commit()
        
        flash(message=Markup(f"Account '{email}' has been verified!"), category="success")
        return redirect("/login")
    except:
        flash("Email link expired or invalid!", "error")
        return redirect("/login")


# CHANGE PASSWORD ROUTE
@auth.route("/change-password", methods=["POST"])
@login_required
def change_password():
    # Get input
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    # Check input
    if not password or not confirmation:
        flash("Invalid password!", "error")
        return redirect("/profile")
    elif password != confirmation:
        flash("Passwords don't match!", "error")
        return redirect("/profile")

    # Get user
    user = Users.query.filter_by(id=session.get("user_id")).first()

    if not user:
        flash("Error updating password", "error")
        return redirect("/profile")

    # Update password
    user.password = generate_password_hash(password)
    db.session.commit()

    session.clear()
    flash("Password updated successfully!", "success")
    return redirect("/login")


# FORGOT PASSWORD ROUTE
@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    # Check if already logged in
    if session.get("user_id") is not None:
        flash("Already logged in!", "error")
        return redirect("/")

    # POST
    if request.method == "POST":
        # Get data
        email = request.form.get("email")

        # Check input
        if not email or not valid_email(email):
            flash("Invalid email!", "error")
            return redirect(request.referrer)
        
        # Check account existence
        user = Users.query.filter_by(email=email).first()
        if not user:
            flash("Account does not exist!", "error")
            return redirect(request.referrer)
        
        # Send confirmation email
        token = create_email_token(email)
        subject = "TMDb: Reset Password"
        link = url_for("auth.reset_password", token=token, _external=True)
        html = render_template("reset-password-email.html", link=link)

        send_email(subject, email, html)

        flash(message=f"An email to reset password is sent to {email}", category="success")
        return redirect(url_for("auth.forgot_password"))
    
    # GET 
    return render_template("forgot-password.html")


# RESET PASSWORD ROUTE
@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    # Check if already logged in
    if session.get("user_id") is not None:
        flash("Already logged in!", "error")
        return redirect("/") 
    
    try:
        # Parse token
        email = parse_email_token(token, 5400)
        
        # Check if account exists
        user = Users.query.filter_by(email=email).first()
        if not user:
            flash("Error changing password!", "error")
            return redirect(url_for("auth.login"))
        
        if request.method == "POST":
            
            # Check input
            password = request.form.get("password")
            confirmation = request.form.get("confirm")

            if not password or not confirmation:
                flash("Error changing password!", "error")
                return redirect(request.referrer)
            elif password != confirmation:
                flash("Passwords mismatch!", "error")
                return redirect(request.referrer)
            elif check_password_hash(user.password, password):
                flash("New password same as old one!", "error")
                return redirect(request.referrer)
            # Update password
            user.password = generate_password_hash(password)
            db.session.commit()

            flash(message=f"Password changed for {email}", category="success")
            return redirect(url_for("auth.login"))
        
         # GET
        return render_template("reset-password.html", token=token)
    
    except:
        flash("Link expired or invalid!", "error")
        return redirect(url_for("auth.forgot_password"))
   

    
      