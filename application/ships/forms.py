from flask_wtf import FlaskForm
from wtforms import *
from application.ships.models import Ship

class ShipCreateForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1, max=256)])
    cost = IntegerField("Cost", [validators.NumberRange(min=0)])
    command_capable = BooleanField("Command-capable")
    propulsion_type = StringField("Propulsion type", [validators.Length(min=1, max=256)])
    move = IntegerField("Move", [validators.NumberRange(min=0)])
    delta_v = IntegerField("Delta-v", [validators.NumberRange(min=0)])
    evasion_passive = IntegerField("Passive evasion")
    evasion_active = IntegerField("Active evasion")
    evasion_endurance = IntegerField("Evasion endurance", [validators.Optional(), validators.NumberRange(min=0)])
    integrity = IntegerField("Integrity", [validators.NumberRange(min=0)])
    primary_facing = StringField("Primary facing", [validators.Length(min=1, max=256)])
    armor_front = IntegerField("Front armor", [validators.NumberRange(min=0)])
    armor_sides = IntegerField("Side armor", [validators.NumberRange(min=0)])
    armor_back = IntegerField("Rear armor", [validators.NumberRange(min=0)])
    weapon1_name = StringField("Weapon 1", [validators.Optional(), validators.Length(min=1, max=256)])
    weapon2_name = StringField("Weapon 2", [validators.Optional(), validators.Length(min=1, max=256)])
    weapon3_name = StringField("Weapon 3", [validators.Optional(), validators.Length(min=1, max=256)])

    class Meta:
        csrf = False

# The update form is currently identical to the create form. If they are going to stay the same,
# the update form can be removed and the create form used in its place as WTForms allows prefilling
# the fields in the case of updating an existing ship without any difference in the form definition.
class ShipUpdateForm(FlaskForm):
    name = StringField("Name")
    cost = IntegerField("Cost")
    command_capable = BooleanField("Command-capable")
    propulsion_type = StringField("Propulsion type")
    move = IntegerField("Move")
    delta_v = IntegerField("Delta-v")
    evasion_passive = IntegerField("Passive evasion")
    evasion_active = IntegerField("Active evasion")
    evasion_endurance = IntegerField("Evasion endurance")
    integrity = IntegerField("Integrity")
    primary_facing = StringField("Primary facing")
    armor_front = IntegerField("Front armor")
    armor_sides = IntegerField("Side armor")
    armor_back = IntegerField("Rear armor")
    weapon1_name = StringField("Weapon 1")
    weapon2_name = StringField("Weapon 2")
    weapon3_name = StringField("Weapon 3")

    class Meta:
        csrf = False