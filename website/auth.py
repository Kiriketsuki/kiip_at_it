# imports
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login.utils import logout_user
from sqlalchemy.engine import url
from sqlalchemy.sql import func
from sqlalchemy.sql.functions import user
from .models import User, Note
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint("auth", __name__)

# default account page
@auth.route("/account")
def account():
    if not current_user.is_authenticated:
        return render_template("sign_up_login.html")
    else:
        variables = {"user": current_user}
        print(func.count(current_user.notes))
        return render_template("account.html", variables = variables)

# login page
@auth.route("/login", methods = ["GET", "POST"])
def login():
    # when the webpage gets updated
    if request.method == "POST":
        # get data from login form
        data = request.form
        email = data.get("email")
        password = data.get("password")

        # get user from db via email
        user = User.query.filter_by(email = email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category = "success")
                login_user(user, remember = True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again", category = "error")
        else:
            flash("Email does not exist. Please try again, or proceed to sign up", category = "error")

    return render_template("login.html")

# logout button
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Successfully logged out. See you again!", category = "success")
    return redirect(url_for("auth.login"))

# signup page
@auth.route("/sign_up", methods = ["GET", "POST"])
def sign_up():
    # when the webpage gets updated
    if request.method == "POST":
        # get data from sign up form
        data = request.form
        email = data.get("email")
        username = data.get("username")
        password1 = data.get("password1")
        password2 = data.get("password2")

        # get user from db via email
        user = User.query.filter_by(email = email).first()

        if user:
            flash("Email already registered", category = "error")
        elif len(email) < 4:
            flash("Enter a valid email", category = "error")
        elif len(username) < 2:
            flash("Enter a valid username", category = "error")
        elif password1 != password2:
            flash("Make sure you entered the same password twice", category = "error")
        elif len(password1) < 8:
            flash("Password needs to be longer than 8 characters", category = "error")
        else:
            new_user = User(email = email, username = username, password = generate_password_hash(password1, method = "sha256"))
            db.session.add(new_user)
            db.session.commit()
            new_note = Note(content = "Use this website", user_id = new_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Account created! Please proceed to login.", category = "success")
            return redirect(url_for("auth.login"))


    return render_template("sign_up.html")