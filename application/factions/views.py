from flask import render_template, request, redirect, url_for

from application import app, db, login_required
from application.factions.models import Faction
from application.factions.forms import FactionCreateForm
from application.ships.models import Ship

# Page for displaying factions and their information
@app.route("/factions/", methods=["GET"])
def factions_index():
    # Query faction info
    factions = Faction.query.all()
    for faction in factions:
        faction.faction_info.update()

    return render_template("factions/list.html", factions = factions)

# Page for creating a faction
@app.route("/factions/new/", methods=["GET"])
@login_required(role="ADMIN")
def factions_create_form():
    return render_template("factions/new.html", form = FactionCreateForm())

# Adds a faction
@app.route("/factions/", methods=["POST"])
@login_required(role="ADMIN")
def factions_create():
    form = FactionCreateForm(request.form)

    # Check validity of input. If input is not valid, return to the faction creation page.
    if not form.validate():
        return render_template("factions/new.html", form = form)

    faction = Faction(form.name.data)

    db.session().add(faction)
    db.session().commit()

    return redirect(url_for("factions_index"))

# Page for updating an existing faction
@app.route("/factions/update/<faction_id>/")
@login_required(role="ADMIN")
def faction_update_form(faction_id):
    faction = Faction.query.get(faction_id)
    form = FactionCreateForm(obj = faction)
    
    return render_template("factions/update.html", form = form, faction = faction)

# Updates the faction wtih the given primary key
@app.route("/factions/update/<faction_id>/", methods=["POST"])
@login_required(role="ADMIN")
def faction_update(faction_id):
    form = FactionCreateForm(request.form)

    faction = Faction.query.get(faction_id)
    # Check validity of input. If input is not valid, return to the ship update page.
    if not form.validate():
        return render_template("factions/update.html", form = form, faction = faction)
    
    faction.name = form.name.data

    db.session().commit()

    return redirect(url_for("factions_index"))

# Removes the faction with the given primary key. Ships belonging to this faction are NOT
# removed, but the associations are.
@app.route("/factions/remove/<faction_id>/", methods=["POST"])
@login_required(role="ADMIN")
def factions_remove(faction_id):
    faction = Faction.query.filter_by(id = faction_id).first()
    # Not very optimal, queries all ships
    ships = Ship.query.all()
    for ship in ships:
        if faction in ship.factions:
            ship.factions.remove(faction)
    
    Faction.query.filter(Faction.id == faction_id).delete()    

    db.session.commit()
    return redirect(url_for("factions_index"))
