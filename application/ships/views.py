from application import app
from flask import render_template, request

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ships/new/")
def ships_form():
    return render_template("ships/new.html")

# This will display a list of existing ships
#@app.route("/ships/")

# This doesn't actually take the required information to make a ship yet, or do anything with it
@app.route("/ships/", methods=["POST"])
def ships_create():
    print(request.form.get("name"))
    return "hello world!"