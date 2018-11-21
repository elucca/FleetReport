from flask import render_template, request, redirect, url_for
from flask_login import login_required

from application import app, db
from application.weapons.models import *
from application.weapons.forms import *

# Adds a laser to a ship
@app.route("/ships/<ship_id>/weapons/laser", methods=["POST"])
@login_required
def laser_create():
    form = LaserCreateForm(request.form)

    laser = Laser(form.name.data, form.dmg_missile.data, ship_id)

    db.session().add(laser)
    db.session.()commit()

    return redirect(url_for("ships_index"))