from flask_wtf import FlaskForm
from wtforms import validators, StringField, IntegerField, BooleanField
from application.factions.models import Faction

class FactionCreateForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1, max=256)])

    class Meta:
        csrf = False