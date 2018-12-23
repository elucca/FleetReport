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

@app.route("/ships/<ship_id>/weapons/laser/<laser_id>/createrangepoint", methods=["GET"])
@login_required(role="ADMIN")
def laser_range_point_create_form(ship_id, laser_id):
    laser = Laser.query.get(laser_id)
    return render_template("weapons/createlaserrangepoint.html", form = LaserRangePointCreateForm(), laser = laser)

@app.route("/ships/<ship_id>/weapons/missile", methods=["GET"])
@login_required(role="ADMIN")
def missile_create_form(ship_id):
    ship = Ship.query.get(ship_id)
    return render_template("weapons/createmissile.html", form = MissileCreateForm(), ship = ship)

@app.route("/ships/<ship_id>/weapons/CIWS", methods=["GET"])
@login_required(role="ADMIN")
def CIWS_create_form(ship_id):
    ship = Ship.query.get(ship_id)
    return render_template("weapons/createciws.html", form = CIWSCreateForm(), ship = ship)

@app.route("/ships/<ship_id>/weapons/areamissile", methods=["GET"])
@login_required(role="ADMIN")
def area_missile_create_form(ship_id):
    ship = Ship.query.get(ship_id)
    return render_template("weapons/createareamissile.html", form = AreaMissileCreateForm(), ship = ship)

@app.route("/ships/<ship_id>/weapons/ewar", methods=["GET"])
@login_required(role="ADMIN")
def ewar_create_form(ship_id):
    ship = Ship.query.get(ship_id)
    return render_template("weapons/createewar.html", form = EwarCreateForm(), ship = ship)

@app.route("/ships/<ship_id>/weapons/ewar/<ewar_id>/createability", methods=["GET"])
@login_required(role="ADMIN")
def ewar_ability_create_form(ship_id, ewar_id):
    ewar = Ewar.query.get(ewar_id)
    return render_template("weapons/createewarability.html", form = EwarAbilityCreateForm(), ewar = ewar)

# Post methods for adding different kinds of weapons

@app.route("/ships/<ship_id>/weapons/laser", methods=["POST"])
@login_required(role="ADMIN")
def laser_create(ship_id):
    form = LaserCreateForm(request.form)

    # Replace with some more sensible redirect back to the form
    if not form.validate():
        return redirect(url_for("ships_info", ship_id = ship_id))

    laser = Laser(form.name.data, form.turreted.data, form.laser_dmg_missile.data, ship_id)

    db.session().add(laser)
    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/laser/<laser_id>/", methods=["POST"])
@login_required(role="ADMIN")
def add_laser_range_point(ship_id, laser_id):
    form = LaserRangePointCreateForm(request.form)

    if not form.validate():
        return redirect(url_for("ships_info", ship_id = ship_id))

    range_point = LaserRangePoint(form.lrange.data, form.dmg.data, laser_id)
    db.session().add(range_point)
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

@app.route("/ships/<ship_id>/weapons/CIWS", methods=["POST"])
@login_required(role="ADMIN")
def CIWS_create(ship_id):
    form = CIWSCreateForm(request.form)
    
    # Replace with some more sensible redirect back to the form
    if not form.validate():
        return redirect(url_for("ships_info", ship_id = ship_id))

    ciws = CIWS(form.name.data, form.dmg_missile.data, form.dmg_ship.data, ship_id)

    db.session().add(ciws)
    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/areamissile", methods=["POST"])
@login_required(role="ADMIN")
def area_missile_create(ship_id):
    form = AreaMissileCreateForm(request.form)
    
    # Replace with some more sensible redirect back to the form
    if not form.validate():
        return redirect(url_for("ships_info", ship_id = ship_id))

    area_missile = AreaMissile(form.name.data, form.am_range.data, form.dmg_missile.data, 
    form.dmg_ship.data, ship_id)

    db.session().add(area_missile)
    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/ewar", methods=["POST"])
@login_required(role="ADMIN")
def ewar_create(ship_id):
    form = EwarCreateForm(request.form)
    
    # Replace with some more sensible redirect back to the form
    if not form.validate():
        return redirect(url_for("ships_info", ship_id = ship_id))

    ewar = Ewar(form.name.data, ship_id)

    db.session().add(ewar)
    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/ewar/<ewar_id>/", methods=["POST"])
@login_required(role="ADMIN")
def add_ewar_ability(ship_id, ewar_id):
    form = EwarAbilityCreateForm(request.form)

    if not form.validate():
        return redirect(url_for("ships_info", ship_id = ship_id))

    ewar_ability = EwarAbility(form.erange.data, form.ability.data, ewar_id)
    db.session().add(ewar_ability)
    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

## Form pages for updating different types of weapons

@app.route("/ships/<ship_id>/weapons/laser/update/<laser_id>")
@login_required(role="ADMIN")
def laser_update_form(laser_id, ship_id):
    laser = Laser.query.get(laser_id)
    form = LaserCreateForm(obj = laser)
    
    return render_template("weapons/updatelaser.html", form = form, laser = laser)

# Not currently used. Laser range points have so little data it's pretty expedient to just remove
# and add one.
@app.route("/ships/<ship_id>/weapons/laser/update/<laser_id>/<laserrangepoint_id>")
@login_required(role="ADMIN")
def laser_range_point_update_form(laser_id, laserrangepoint_id):
    rangepoint = LaserRangePoint.query.get(laserrangepoint_id)
    form = LaserRangePointCreateForm(obj = rangepoint)

    return render_template("weapons/updatelaserrangepoint.html")

@app.route("/ships/<ship_id>/weapons/missile/update/<missile_id>")
@login_required(role="ADMIN")
def missile_update_form(missile_id, ship_id):
    missile = Missile.query.get(missile_id)
    form = MissileCreateForm(obj = missile)
    
    return render_template("weapons/updatemissile.html", form = form, missile = missile)

@app.route("/ships/<ship_id>/weapons/CIWS/update/<ciws_id>")
@login_required(role="ADMIN")
def CIWS_update_form(ciws_id, ship_id):
    ciws = CIWS.query.get(ciws_id)
    form = CIWSCreateForm(obj = ciws)
    
    return render_template("weapons/updateciws.html", form = form, ciws = ciws)

@app.route("/ships/<ship_id>/weapons/areamissile/update/<areamissile_id>")
@login_required(role="ADMIN")
def area_missile_update_form(areamissile_id, ship_id):
    areamissile = AreaMissile.query.get(areamissile_id)
    form = AreaMissileCreateForm(obj = areamissile)
    
    return render_template("weapons/updateareamissile.html", form = form, areamissile = areamissile)

@app.route("/ships/<ship_id>/weapons/ewar/update/<ewar_id>")
@login_required(role="ADMIN")
def ewar_update_form(ewar_id, ship_id):
    ewar = Ewar.query.get(ewar_id)
    form = EwarCreateForm(obj = ewar)
    
    return render_template("weapons/updateewar.html", form = form, ewar = ewar)

@app.route("/ships/<ship_id>/weapons/ewar/update/<ewar_id>/<ewarability_id>")
@login_required(role="ADMIN")
def ewar_ability_update_form(ewar_id, ewarability_id):
    ability = EwarAbility.query.get(ewarability_id)
    form = EwarAbilityCreateForm(obj = ability)

    return render_template("weapons/updateewarability.html", form = form, ewarability = ability)

## Post methods for updating different types of weapons

@app.route("/ships/<ship_id>/weapons/laser/update/<laser_id>", methods=["POST"])
@login_required(role="ADMIN")
def laser_update(laser_id, ship_id):
    form = LaserCreateForm(request.form)
    laser = Laser.query.get(laser_id)

    laser.name = form.name.data
    laser.turreted = form.turreted.data
    laser.laser_dmg_missile = form.laser_dmg_missile.data
    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/laser/update/<laser_id>/<laserrangepoint_id>", methods=["POST"])
@login_required(role="ADMIN")
def laser_range_point_update(ship_id, laser_id, laserrangepoint_id):
    form = LaserRangePointCreateForm(request.form)
    rangepoint = LaserRangePoint.query.get(laserrangepoint_id)

    rangepoint.lrange = form.lrange.data
    rangepoint.dmg = form.dmg.data
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

@app.route("/ships/<ship_id>/weapons/CIWS/update/<ciws_id>", methods=["POST"])
@login_required(role="ADMIN")
def CIWS_update(ciws_id, ship_id):
    form = CIWSCreateForm(request.form)
    ciws = CIWS.query.get(ciws_id)

    ciws.name = form.name.data 
    ciws.dmg_missile = form.dmg_missile.data
    ciws.dmg_ship = form.dmg_ship.data
    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/areamissile/update/<areamissile_id>", methods=["POST"])
@login_required(role="ADMIN")
def area_missile_update(areamissile_id, ship_id):
    form = AreaMissileCreateForm(request.form)
    area_missile = AreaMissile.query.get(areamissile_id)

    area_missile.name = form.name.data 
    area_missile.am_range = form.am_range.data
    area_missile.dmg_missile = form.dmg_missile.data
    area_missile.dmg_ship = form.dmg_ship.data

    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/ewar/update/<ewar_id>", methods=["POST"])
@login_required(role="ADMIN")
def ewar_update(ewar_id, ship_id):
    form = EwarCreateForm(request.form)
    ewar = Ewar.query.get(ewar_id)

    ewar.name = form.name.data
    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/ewar/update/<ewar_id>/<ewarability_id>", methods=["POST"])
@login_required(role="ADMIN")
def ewar_ability_update(ship_id, ewar_id, ewarability_id):
    form = EwarAbilityCreateForm(request.form)
    ability = EwarAbility.query.get(ewarability_id)

    ability.ability = form.ability.data
    ability.erange = form.erange.data
    db.session().commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

## Post methods for removing different types of weapons

@app.route("/ships/<ship_id>/weapons/laser/remove/<laser_id>", methods=["POST"])
@login_required(role="ADMIN")
def laser_remove(laser_id, ship_id):
    # Remove range points
    LaserRangePoint.query.filter(LaserRangePoint.laser_id == laser_id).delete()
    Missile.query.filter(Missile.ship_id == ship_id).delete()


    Laser.query.filter(Laser.id == laser_id).delete()
    db.session.commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/laser/update/<laser_id>/<laserrangepoint_id>/remove", methods=["POST"])
@login_required(role="ADMIN")
def laser_range_point_remove(ship_id, laser_id, laserrangepoint_id):
    LaserRangePoint.query.filter(LaserRangePoint.id == laserrangepoint_id).delete()
    db.session.commit()

    return redirect(url_for("ships_info", ship_id = ship_id))


@app.route("/ships/<ship_id>/weapons/missile/remove/<missile_id>", methods=["POST"])
@login_required(role="ADMIN")
def missile_remove(missile_id, ship_id):
    Missile.query.filter(Missile.id == missile_id).delete()
    db.session.commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/CIWS/remove/<ciws_id>", methods=["POST"])
@login_required(role="ADMIN")
def CIWS_remove(ciws_id, ship_id):
    CIWS.query.filter(CIWS.id == ciws_id).delete()
    db.session.commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/areamissile/remove/<areamissile_id>", methods=["POST"])
@login_required(role="ADMIN")
def area_missile_remove(areamissile_id, ship_id):
    AreaMissile.query.filter(AreaMissile.id == areamissile_id).delete()
    db.session.commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/ewar/remove/<ewar_id>", methods=["POST"])
@login_required(role="ADMIN")
def ewar_remove(ewar_id, ship_id):
    # Remove abilities
    EwarAbility.query.filter(EwarAbility.ewar_id == ewar_id).delete()

    Ewar.query.filter(Ewar.id == ewar_id).delete()
    db.session.commit()

    return redirect(url_for("ships_info", ship_id = ship_id))

@app.route("/ships/<ship_id>/weapons/ewar/update/<ewar_id>/<ewarability_id>/remove", methods=["POST"])
@login_required(role="ADMIN")
def ewar_ability_remove(ship_id, ewar_id, ewarability_id):
    EwarAbility.query.filter(EwarAbility.id == ewarability_id).delete()
    db.session.commit()

    return redirect(url_for("ships_info", ship_id = ship_id))