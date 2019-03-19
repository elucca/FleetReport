from application.ships.models import Ship
import json

def serialize_ships():
    ships = Ship.query.all()
    with open('ships.json', 'w') as outfile:
        #json.dumps(ships)
        pass

class ShipEncoder(json.JSONEncoder):

    def default(self, ship):
        if isinstance(ship, Ship):
            return 
        else:
            super().default(self, ship)

    