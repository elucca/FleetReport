from application import db

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