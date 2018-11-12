from application import app, db
from flask import render_template, request, redirect, url_for
from application.ships.models import Ship
from application.ships.forms import *

@app.route("/")
def index():
    return render_template("index.html")

# Page for creating a new ship
@app.route("/ships/new/")
def ships_create_form():
    return render_template("ships/new.html", form = ShipCreateForm())

# Page for updating an existing ship
@app.route("/ships/update/<ship_id>/")
def ships_update_form(ship_id):
    return render_template("ships/update.html", form = ShipUpdateForm(), ship = Ship.query.get(ship_id))

# Page for listing existing ships
@app.route("/ships/", methods=["GET"])
def ships_index():
    return render_template("ships/list.html", ships = Ship.query.all())

# Adds a new ship to database
@app.route("/ships/", methods=["POST"])
def ships_create():
    form = ShipCreateForm(request.form)
    
    ship = Ship(form.name.data, form.cost.data, form.command_capable.data, form.propulsion_type.data, form.move.data, 
                form.delta_v.data, form.evasion_passive.data, form.evasion_active.data, form.evasion_endurance.data, 
                form.integrity.data, form.primary_facing.data, form.armor_front.data, form.armor_sides.data, 
                form.armor_back.data, form.weapon1_name.data, form.weapon2_name.data, form.weapon3_name.data)

    db.session().add(ship)
    db.session().commit()

    return redirect(url_for("ships_index"))


# Updates a ship with given primary key
# It updates everything regardless of it it was changed, but this shouldn't be an issue
@app.route("/ships/<ship_id>/", methods=["POST"])
def ships_update(ship_id):
    form = ShipUpdateForm(request.form)

    """
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
    db.session().commit()
    """

    return redirect(url_for("ships_index"))