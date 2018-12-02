from flask import render_template, request, redirect, url_for

from application import app, db, login_required
from application.ships.models import Ship
from application.weapons.models import *
from application.weapons.forms import *

## Form pages for adding different kinds of weapons

@app.route("/ships/<ship_id>/weapons/laser", methods=["GET"])
@login_required(role="ADMIN")
def laser_create_form(ship_id):
    ship = Ship.query.get(ship_id)
    return render_template("weapons/createlaser.html", form = LaserCreateForm(), ship = ship)

@app.route("/ships/<ship_id>/weapons/missile", methods=["GET"])
@login_required(role="ADMIN")
def missile_create_form(ship_id):
    ship = Ship.query.get(ship_id)
    return render_template("weapons/createmissile.html", form = MissileCreateForm(), ship = ship)


# Post methods for adding different kinds of weapons

@app.route("/ships/<ship_id>/weapons/laser", methods=["POST"])
@login_required(role="ADMIN")
def laser_create(ship_id):
    form = LaserCreateForm(request.form)

    # Replace with some more sensible redirect back to the form
    if not form.validate():
        return redirect(url_for("ships_info", ship_id = ship_id))

    laser = Laser(form.name.data, form.laser_dmg_missile.data, ship_id)

    db.session().add(laser)
    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/missile", methods=["POST"])
@login_required(role="ADMIN")
def missile_create(ship_id):
    form = MissileCreateForm(request.form)
    
    # Replace with some more sensible redirect back to the form
    if not form.validate():
        return redirect(url_for("ships_info", ship_id = ship_id))

    missile = Missile(form.name.data, form.volley.data, form.stores.data, ship_id)

    db.session().add(missile)
    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

## Pages for updating different types of weapons

# Page for updating a laser
@app.route("/ships/<ship_id>/weapons/laser/update/<laser_id>")
@login_required(role="ADMIN")
def laser_update_form(laser_id, ship_id):
    laser = Laser.query.get(laser_id)
    form = LaserCreateForm(obj = laser)
    
    return render_template("weapons/updatelaser.html", form = form, laser = laser)

# Page for updating a missile
@app.route("/ships/<ship_id>/weapons/missile/update/<missile_id>")
@login_required(role="ADMIN")
def missile_update_form(missile_id, ship_id):
    missile = Missile.query.get(missile_id)
    form = MissileCreateForm(obj = missile)
    
    return render_template("weapons/updatemissile.html", form = form, missile = missile)

## Post methods for updating different types of weapons

# Updates a laser with given primary key
@app.route("/ships/<ship_id>/weapons/laser/update/<laser_id>", methods=["POST"])
@login_required(role="ADMIN")
def laser_update(laser_id, ship_id):
    form = LaserCreateForm(request.form)
    laser = Laser.query.get(laser_id)

    laser.name = form.name.data
    laser.laser_dmg_missile = form.laser_dmg_missile.data
    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/missile/update/<missile_id>", methods=["POST"])
@login_required(role="ADMIN")
def missile_update(missile_id, ship_id):
    form = MissileCreateForm(request.form)
    missile = Missile.query.get(missile_id)

    missile.name = form.name.data 
    missile.volley = form.volley.data
    missile.stores = form.stores.data
    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

## Post methods for removing different types of weapons

# Removes a laser
@app.route("/ships/<ship_id>/weapons/laser/remove/<laser_id>", methods=["POST"])
@login_required(role="ADMIN")
def laser_remove(laser_id, ship_id):
    Laser.query.filter(Laser.id == laser_id).delete()
    db.session.commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

# Removes a missile
@app.route("/ships/<ship_id>/weapons/missile/remove/<missile_id>", methods=["POST"])
@login_required(role="ADMIN")
def missile_remove(missile_id, ship_id):
    Missile.query.filter(Missile.id == missile_id).delete()
    db.session.commit()

    return redirect(url_for("ships_info", ship_id = ship_id))