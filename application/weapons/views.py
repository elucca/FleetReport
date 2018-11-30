from flask import render_template, request, redirect, url_for

from application import app, db, login_required
from application.ships.models import Ship
from application.weapons.models import *
from application.weapons.forms import *

# Form pages for adding different kinds of weapons

@app.route("/ships/<ship_id>/weapons/laser", methods=["GET"])
@login_required(role="ADMIN")
def laser_create_form(ship_id):
    ship = Ship.query.get(ship_id)
    return render_template("weapons/createlaser.html", form = LaserCreateForm(obj = ship), ship = ship)

@app.route("/ships/<ship_id>/weapons/missile", methods=["GET"])
@login_required(role="ADMIN")
def missile_create_form(ship_id):
    ship = Ship.query.get(ship_id)
    return render_template("weapons/createmissile.html", form = MissileCreateForm(obj = ship), ship = ship)


# Post methods for adding different kinds of weapons

@app.route("/ships/<ship_id>/weapons/laser", methods=["POST"])
@login_required(role="ADMIN")
def laser_create(ship_id):
    form = LaserCreateForm(request.form)

    # Replace with some more sensible redirect back to the form
    if not form.validate():
        return redirect(url_for("ships_index"))

    laser = Laser(form.laser_name.data, form.laser_dmg_missile.data, ship_id)

    db.session().add(laser)
    db.session().commit()

    return redirect(url_for("ships_index"))

@app.route("/ships/<ship_id>/weapons/missile", methods=["POST"])
@login_required(role="ADMIN")
def missile_create(ship_id):
    form = MissileCreateForm(request.form)
    
    # Replace with some more sensible redirect back to the form
    if not form.validate():
        return redirect(url_for("ships_index"))

    missile = Missile(form.missile_name.data, form.volley.data, form.stores.data, ship_id)

    db.session().add(missile)
    db.session().commit()

    return redirect(url_for("ships_index"))