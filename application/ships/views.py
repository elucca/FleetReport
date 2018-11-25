from flask import render_template, request, redirect, url_for

from flask_login import login_required

from application import app, db
from application.ships.models import Ship
from application.ships.forms import ShipCreateForm
from application.factions.models import Faction, factionship
from application.weapons.models import *

@app.route("/")
def index():
    return render_template("index.html")

# Page for creating a new ship
@app.route("/ships/new/")
@login_required
def ships_create_form():
    form = ShipCreateForm()

    # Get existing factions and add them to a multiple choice field in the form
    form.factions.choices = _get_factions_list_()

    return render_template("ships/new.html", form = form)

# Page for updating an existing ship
@app.route("/ships/update/<ship_id>/")
@login_required
def ships_update_form(ship_id):
    ship = Ship.query.get(ship_id)
    return render_template("ships/update.html", form = ShipCreateForm(obj = ship), ship = ship)

# Page for listing existing ships
@app.route("/ships/", methods=["GET"])
def ships_index():
    return render_template("ships/list.html", ships = Ship.query.all(), factions = Faction.query.all())

# Page for showing detailed information of selected ship
@app.route("/ships/<ship_id>/", methods=["GET"])
def ships_info(ship_id):
    return render_template("ships/shipinfo.html", ship = Ship.query.get(ship_id))

# Adds a new ship to database
@app.route("/ships/", methods=["POST"])
@login_required
def ships_create():
    form = ShipCreateForm(request.form)

    # Check validity of input. If input is not valid, return to the ship creation page.
    form.factions.choices = _get_factions_list_()
    if not form.validate_on_submit():
        return render_template("ships/new.html", form = form)

    ship = Ship(form.name.data, form.cost.data, form.command_capable.data, form.propulsion_type.data, form.move.data, 
                form.delta_v.data, form.evasion_passive.data, form.evasion_active.data, form.evasion_endurance.data, 
                form.integrity.data, form.primary_facing.data, form.armor_front.data, form.armor_sides.data, 
                form.armor_back.data)

    db.session().add(ship)
    db.session().commit()

    # Add ship entry to factionships association table
    # For some reason the form returns the id of the faction, which is ok
    # This is kinda spaghetti
    faction_ids = form.factions.data
    for faction_id in faction_ids:
        faction = Faction.query.filter_by(id = faction_id).first()
        faction.ships.append(ship)
        db.session.add(faction)
        db.session.commit()
    
    return redirect(url_for("ships_index"))


# Updates a ship with given primary key
# It updates everything regardless of whether it was changed, but this shouldn't be an issue
@app.route("/ships/update/<ship_id>/", methods=["POST"])
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
    db.session().commit()

    return redirect(url_for("ships_index"))

@app.route("/ships/remove/<ship_id>/", methods=["POST"])
@login_required
def ships_remove(ship_id):
    # Remove weapons (SQLALchemy cascade not working)
    Laser.query.filter(ship_id == ship_id).delete()
    Missile.query.filter(ship_id == ship_id).delete()
    CIWS.query.filter(ship_id == ship_id).delete()
    AreaMissile.query.filter(ship_id == ship_id).delete()
    Ewar.query.filter(ship_id == ship_id).delete()

    # Remove associative entries with Faction (SQlAlchemy cascade not working)
    ship = Ship.query.get(ship_id)
    factions = Faction.query.all()
    for faction in factions:
        faction.ships.remove(ship)

    Ship.query.filter(Ship.id == ship_id).delete()    

    db.session.commit()
    return redirect(url_for("ships_index"))

# Gets a list of factions for use in ship creation/update forms
def _get_factions_list_():
    factions = Faction.query.all()
    factions_list=[(f.id, f.name) for f in factions]

    return factions_list