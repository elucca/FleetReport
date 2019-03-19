from application import db
from application.models import BaseModel
 
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import desc

# Abstract base model for weapon models
class Weapon(BaseModel):
    __abstract__ = True
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
 
    @declared_attr
    def ship_id(cls):
        return db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False, index=True)
 
    def __init__(self, name, ship_id):
        self.name = name
        self.ship_id = ship_id
 
class Laser(Weapon):
    turreted = db.Column(db.Boolean, nullable=False)
    laser_dmg_missile = db.Column(db.String(256), nullable=False)

    rangepoints = db.relationship('LaserRangePoint', backref='laser', order_by="desc(LaserRangePoint.lrange)", lazy=True)

    # Fields for serialization
    _default_fields = [
        "name",
        "turreted",
        "laser_dmg_missile",
        "rangepoints"
    ]

    _hidden_fields = [
        "id"
    ]
 
    def __init__(self, name, turreted, dmg_missile, ship_id):
        super().__init__(name, ship_id)
        self.turreted = turreted
        self.laser_dmg_missile = dmg_missile

class LaserRangePoint(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    lrange = db.Column(db.Integer, nullable=False)
    dmg = db.Column(db.Integer, nullable=False)
    laser_id = db.Column(db.Integer, db.ForeignKey('laser.id'), nullable=False, index=True)

    # Fields for serialization
    _default_fields = [
        "lrange",
        "dmg"
    ]

    _hidden_fields = [
        "id",
        "laser_id"
    ]

    def __init__(self, lrange, dmg, laser_id):
        self.lrange = lrange
        self.dmg = dmg
        self.laser_id = laser_id
 
class Missile(Weapon):
    volley = db.Column(db.Integer, nullable=False)
    stores = db.Column(db.Integer, nullable=False)

    # Fields for serialization
    _default_fields = [
        "volley",
        "stores"
    ]

    _hidden_fields = [
        "id"
    ]

 
    def __init__(self, name, volley, stores, ship_id):
        super().__init__(name, ship_id)
        self.volley = volley
        self.stores = stores
 
class CIWS(Weapon):
    dmg_missile = db.Column(db.String(256), nullable=False)
    dmg_ship = db.Column(db.String(256), nullable=False)

    # Fields for serialization
    _default_fields = [
        "dmg_missile",
        "dmg_ship"
    ]

    _hidden_fields = [
        "id"
    ]
 
    def __init__(self, name, dmg_missile, dmg_ship, ship_id):
        super().__init__(name, ship_id)
        self.dmg_missile = dmg_missile
        self.dmg_ship = dmg_ship
 
class AreaMissile(Weapon):
    am_range = db.Column(db.Integer, nullable=False)
    dmg_missile = db.Column(db.String(256), nullable=False)
    dmg_ship = db.Column(db.String(256), nullable=False)

    # Fields for serialization
    _default_fields = [
        "am_range",
        "dmg_missile",
        "dmg_ship"
    ]

    _hidden_fields = [
        "id"
    ]
 
    def __init__(self, name, am_range, dmg_missile, dmg_ship, ship_id):
        super().__init__(name, ship_id)
        self.am_range = am_range
        self.dmg_missile = dmg_missile
        self.dmg_ship = dmg_ship
 
class Ewar(Weapon):
    abilities = db.relationship('EwarAbility', backref='ewar', lazy=True)

    # Fields for serialization
    _default_fields = [
        "abilities"
    ]

    _hidden_fields = [
        "id"
    ]

    def __init__(self, name, ship_id):
        super().__init__(name, ship_id)

class EwarAbility(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    erange = db.Column(db.Integer, nullable=False)
    ability = db.Column(db.String(256), nullable=False)
    ewar_id = db.Column(db.Integer, db.ForeignKey('ewar.id'), nullable=False, index=True)

    # Fields for serialization
    _default_fields = [
        "erange",
        "ability"
    ]

    _hidden_fields = [
        "id",
        "ewar_id"
    ]

    def __init__(self, erange, ability, ewar_id):
        self.erange = erange
        self.ability = ability
        self.ewar_id = ewar_id
