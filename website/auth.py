from flask import Blueprint, render_template, request, flash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods = ["GET", "POST"])
def login():
    data = request.form
    print(data)
    return render_template("login.html", test = "Testing")

@auth.route("/logout")
def logout():
    return "<p>Logout</p>"

@auth.route("/sign_up", methods = ["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if len(email) < 4:
            flash("Enter a valid email", category = "error")
        elif len(username) < 2:
            flash("Enter a valid username", category = "error")
        elif password1 != password2:
            flash("Make sure you entered the same password twice", category = "error")
        elif len(password1) < 8:
            flash("Password needs to be longer than 8 characters", category = "error")
        else:
            flash("Account created! Please proceed to login.", category = "success")
            # add user to database
    return render_template("sign_up.html")