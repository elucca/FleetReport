from application import app, db
from flask import render_template, request
from application.ships.models import Ship

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
    ship = Ship(request.form.get("name"), request.form.get("cost"), request.form.get("propulsion_type"), request.form.get("move"), 
                request.form.get("delta_v"), request.form.get("evasion_passive"), request.form.get("evasion_active"), 
                request.form.get("evasion_endurance"), request.form.get("armor_front"), request.form.get("armor_sides"), 
                request.form.get("armor_back"), request.form.get("weapon1_name"), request.form.get("weapon2_name"), 
                request.form.get("weapon2_name")
               )

    db.session().add(ship)
    db.session().commit()

    return "hello world!"