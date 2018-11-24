from flask import render_template, request, redirect, url_for
from flask_login import login_required

from application import app, db
from application.factions.models import Faction
from application.factions.forms import FactionCreateForm

# Page for displaying factions and their information
@app.route("/factions/", methods=["GET"])
def factions_index():
    return render_template("factions/list.html", factions = Faction.query.all())

# Page for creating a faction
@app.route("/factions/new/", methods=["GET"])
@login_required
def factions_create_form():
    return render_template("factions/new.html", form = FactionCreateForm())

# Address for adding a faction
@app.route("/factions/", methods=["POST"])
@login_required
def factions_create():
    form = FactionCreateForm(request.form)

    # Check validity of input. If input is not valid, return to the faction creation page.
    if not form.validate():
        return render_template("factions/new.html", form = form)

    faction = Faction(form.name.data)

    db.session().add(faction)
    db.session().commit()

    return redirect(url_for("factions_index"))