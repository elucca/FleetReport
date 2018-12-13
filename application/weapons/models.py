from application import db

# The weapon classes really should inherit from this abstract base class, but they
# currently don't because I can't invoke the correct rituals to make SQLAlchemy
# work right with this.
"""
class Weapon(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    def __init__(self, name, ship_id):
        self.name = name
        self.ship_id = ship_id
"""

# This class is a stub that is missing data that will eventually be provided in
# another table'
class Laser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    laser_dmg_missile = db.Column(db.String(256), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False, index=True)

    def __init__(self, name, dmg_missile, ship_id):
        self.name = name
        self.laser_dmg_missile = dmg_missile
        self.ship_id = ship_id

class Missile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    volley = db.Column(db.Integer, nullable=False)
    stores = db.Column(db.Integer, nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False, index=True)

    def __init__(self, name, volley, stores, ship_id):
        self.name = name
        self.ship_id = ship_id
        self.volley = volley
        self.stores = stores

class CIWS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    dmg_missile = db.Column(db.String(256), nullable=False)
    dmg_ship = db.Column(db.String(256), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False, index=True)

    def __init__(self, name, dmg_missile, dmg_ship, ship_id):
        self.name = name
        self.ship_id = ship_id
        self.dmg_missile = dmg_missile
        self.dmg_ship = dmg_ship

class AreaMissile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    am_range = db.Column(db.Integer, nullable=False)
    dmg_missile = db.Column(db.String(256), nullable=False)
    dmg_ship = db.Column(db.String(256), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False, index=True)

    def __init__(self, name, am_range, dmg_missile, dmg_ship, ship_id):
        self.name = name
        self.ship_id = ship_id
        self.am_range = am_range
        self.dmg_missile = dmg_missile
        self.dmg_ship = dmg_ship

# This class is a stub that is missing data that will eventually be provided in
# another table
class Ewar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    ship_id = db.Column(db.Integer, db.ForeignKey('ship.id'), nullable=False, index=True)

    def __init__(self, name, ship_id):
        self.name = name
        self.ship_id = ship_id