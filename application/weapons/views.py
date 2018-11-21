from flask import render_template, request, redirect, url_for
from flask_login import login_required

from application import app, db
from application.ships.models import Ship
from application.weapons.models import *
from application.weapons.forms import *

# Form for adding a laser
@app.route("/ships/<ship_id>/weapons/laser", methods=["GET"])
@login_required
def laser_create_form(ship_id):
    ship = Ship.query.get(ship_id)
    #return render_template("weapons/createlaser.html", form = LaserCreateForm(obj = ship), ship = ship)
    return render_template("weapons/createlaser.html", form = LaserCreateForm(obj = ship), ship = ship)


# Adds a laser to a ship
@app.route("/ships/<ship_id>/weapons/laser", methods=["POST"])
@login_required
def laser_create(ship_id):
    form = LaserCreateForm(request.form)

    laser = Laser(form.laser_name.data, form.laser_dmg_missile.data, ship_id)

    db.session().add(laser)
    db.session().commit()

    return redirect(url_for("ships_index"))