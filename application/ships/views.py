from flask import render_template, request, redirect, url_for

from flask_login import login_required

from application import app, db
from application.ships.models import Ship
from application.ships.forms import *

@app.route("/")
def index():
    return render_template("index.html")

# Page for creating a new ship
@app.route("/ships/new/")
@login_required
def ships_create_form():
    return render_template("ships/new.html", form = ShipCreateForm())

# Page for updating an existing ship
@app.route("/ships/update/<ship_id>/")
@login_required
def ships_update_form(ship_id):
    ship = Ship.query.get(ship_id)
    return render_template("ships/update.html", form = ShipCreateForm(obj = ship), ship = ship)

# Page for listing existing ships
@app.route("/ships/", methods=["GET"])
def ships_index():
    return render_template("ships/list.html", ships = Ship.query.all())

# Adds a new ship to database
@app.route("/ships/", methods=["POST"])
@login_required
def ships_create():
    form = ShipCreateForm(request.form)

    # Check validity of input. If input is not valid, return to the ship creation page.
    if not form.validate():
        return render_template("ships/new.html", form = form)

    
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
@login_required
def ships_update(ship_id):
    form = ShipCreateForm(request.form)

    ship = Ship.query.get(ship_id)
    
    if not form.validate():
        return render_template("ships/update.html", form = form, ship = ship)

    ship.name = form.name.data
    ship.cost = form.cost.data
    ship.command_capable = form.command_capable.data
    ship.propulsion_type = form.propulsion_type.data
    ship.move = form.move.data
    ship.delta_v = form.delta_v.data
    ship.evasion_passive = form.evasion_passive.data
    ship.evasion_active = form.evasion_active.data
    ship.evasion_endurance = form.evasion_endurance.data
    ship.integrity = form.integrity.data
    ship.primary_facing = form.primary_facing.data
    ship.armor_front = form.armor_front.data
    ship.armor_sides = form.armor_sides.data
    ship.armor_back = form.armor_back.data
    ship.weapon1_name = form.weapon1_name.data
    ship.weapon2_name = form.weapon2_name.data
    ship.weapon3_name = form.weapon3_name.data
    db.session().commit()

    return redirect(url_for("ships_index"))