from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, UserCreateForm

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

    # flask-login login function
    login_user(user)
    return redirect(url_for("index"))    

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))    

@app.route("/auth/newuser", methods = ["GET", "POST"])
def auth_newuser():
    if request.method == "GET":
        return render_template("/auth/newuser.html", form = UserCreateForm())

    form = UserCreateForm()
    # Validation goes here

    new_user = User(form.name.data, form.username.data, form.password.data)

    db.session().add(new_user)
    db.session().commit()

    return redirect(url_for("index"))