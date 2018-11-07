from application import app, db
from flask import render_template, request, redirect, url_for
from application.ships.models import Ship

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ships/new/")
def ships_create_form():
    return render_template("ships/new.html")

# Lists existing ships
@app.route("/ships/", methods=["GET"])
def ships_index():
    return render_template("ships/list.html", ships = Ship.query.all())

# Adds a new ship to database
@app.route("/ships/", methods=["POST"])
def ships_create():
    ship = Ship(request.form.get("name"), request.form.get("cost"), request.form.get("command_capable"), 
                request.form.get("propulsion_type"), request.form.get("move"), request.form.get("delta_v"), 
                request.form.get("evasion_passive"), request.form.get("evasion_active"), 
                request.form.get("evasion_endurance"), request.form.get("integrity"), request.form.get("primary_facing"), 
                request.form.get("armor_front"), request.form.get("armor_sides"), request.form.get("armor_back"), 
                request.form.get("weapon1_name"), request.form.get("weapon2_name"), request.form.get("weapon3_name")
               )

    db.session().add(ship)
    db.session().commit()

    return redirect(url_for("ships_index"))

# Updates a ship with given primary key
# Not yet used anywhere
# Currently this just changes everything (except id), does this make sense?
@app.route("/ships/<ship_id>/", methods=["POST"])
def ships_update(ship_id):
    ship = Ship.query.get(ship_id)
    ship.name = request.form.get("name")
    ship.cost = request.form.get("cost")
    ship.command_capable = request.form.get("command_capable")
    ship.propulsion_type = request.form.get("propulsion_type")
    ship.move = request.form.get("move")
    ship.delta_v = request.form.get("delta_v")
    ship.evasion_passive = request.form.get("evasion_passive")
    ship.evasion_active = request.form.get("evasion_active")
    ship.evasion_endurance = request.form.get("evasion_endurance")
    ship.integrity = request.form.get("integrity")
    ship.primary_facing = request.form.get("primary_facing")
    ship.armor_front = request.form.get("armor_front")
    ship.armor_sides = request.form.get("armor_sides")
    ship.armor_back = request.form.get("armor_back")
    ship.weapon1_name = request.form.get("weapon1_name")
    ship.weapon2_name = request.form.get("weapon2_name")
    ship.weapon3_name = request.form.get("weapon3_name")