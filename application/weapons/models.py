from application import db
 
from sqlalchemy.ext.declarative import declared_attr

# Abstract base model for weapon models
class Weapon(db.Model):
    __abstract__ = True
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
 
    @declared_attr
    def ship_id(cls):
        return db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False, index=True)
 
    def __init__(self, name, ship_id):
        self.name = name
        self.ship_id = ship_id
 
# This class is a stub that is missing data that will eventually be provided in
# another table'
class Laser(Weapon):
    laser_dmg_missile = db.Column(db.String(256), nullable=False)
 
    def __init__(self, name, dmg_missile, ship_id):
        super().__init__(name, ship_id)
        self.laser_dmg_missile = dmg_missile
 
class Missile(Weapon):
    volley = db.Column(db.Integer, nullable=False)
    stores = db.Column(db.Integer, nullable=False)
 
    def __init__(self, name, volley, stores, ship_id):
        super().__init__(name, ship_id)
        self.volley = volley
        self.stores = stores
 
class CIWS(Weapon):
    dmg_missile = db.Column(db.String(256), nullable=False)
    dmg_ship = db.Column(db.String(256), nullable=False)
 
    def __init__(self, name, dmg_missile, dmg_ship, ship_id):
        super().__init__(name, ship_id)
        self.dmg_missile = dmg_missile
        self.dmg_ship = dmg_ship
 
class AreaMissile(Weapon):
    am_range = db.Column(db.Integer, nullable=False)
    dmg_missile = db.Column(db.String(256), nullable=False)
    dmg_ship = db.Column(db.String(256), nullable=False)
 
    def __init__(self, name, am_range, dmg_missile, dmg_ship, ship_id):
        super().__init__(name, ship_id)
        self.am_range = am_range
        self.dmg_missile = dmg_missile
        self.dmg_ship = dmg_ship
 
# This class is a stub that is missing data that will eventually be provided in
# another table
class Ewar(Weapon):
    def __init__(self, name, ship_id):
        super().__init__(name, ship_id)
