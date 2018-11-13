from flask import render_template, request, redirect, url_for

from application import app
from application.auth.models import User
from application.auth.forms import LoginForm

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    # For GET:
    if request.method == "GET":
        return render_template("auth/login.html", form = LoginForm())

    # For POST:
    form = LoginForm(request.form)

    # Validation goes here

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/login.html", form = form,
                               error = "No such username or password")


    print("User " + user.name + " login recognized")
    return redirect(url_for("index"))