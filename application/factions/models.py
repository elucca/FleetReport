from application import db

from sqlalchemy.sql import text
from sqlalchemy import orm

# Association table for many-to-many relationship between factions and ships
factionships = db.Table('factionship',
    db.Column('faction_id', db.Integer, db.ForeignKey('faction.id'), primary_key=True),
    db.Column('ship_id', db.Integer, db.ForeignKey('ship.id'), primary_key=True)
)

class Faction(db.Model):
    __tablename__ = 'faction'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    ships = db.relationship('Ship', secondary=factionships, backref=db.backref('factions', lazy=True))

    def __init__(self, name):
        self.name = name

    @orm.reconstructor
    def init_on_load(self):
        self.faction_info = FactionInfo(self)

# This class is a container for various info related to the faction generated from queries, used
# on faction templates.
class FactionInfo():
    def __init__(self, faction):
        self.faction = faction

    def update(self):
        self.ship_count = self.number_of_ships(self.faction)
        self.command_ship_count = self.number_of_command_ships(self.faction)

    def number_of_ships(self, faction):
        stmt = text("SELECT COUNT(ship.id) FROM ship"
                    " LEFT JOIN factionship ON factionship.ship_id = ship.id"
                    " WHERE factionship.faction_id = :faction_id").params(faction_id=faction.id)
        
        resultProxy = db.engine.execute(stmt)
        result = resultProxy.fetchone()[0]
        return result

    def number_of_command_ships(self, faction):
        stmt = text("SELECT COUNT(ship.id) FROM ship"
                    " LEFT JOIN factionship ON factionship.ship_id = ship.id"
                    " WHERE factionship.faction_id = :faction_id"
                    " AND ship.command_capable = 1").params(faction_id=faction.id)
        
        resultProxy = db.engine.execute(stmt)
        result = resultProxy.fetchone()[0]
        return result