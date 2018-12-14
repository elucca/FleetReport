# User stories

- As the game designer, I require an admin account with full access to modifying data.
  - Status: Implemented
  
- As the game designer, I want to add, modify and remove ships and their weapons.
  - Status: Implemented, but laser and ewar data types are 'stubs' in that they don't contain all the data required for the game. This is intended for now.

- As the game designer, I want to add, modify and remove factions
  - Status: In progress
 
- As game designer or playtester, I want to inspect the characteristics of ships.
  - Status: Implemented.

- As game designer or playtester, I want to see the list of ships for a given faction for a quick reference of what ships are available, and their characteristics.
  - Status: Implemented. It may be useful to add some basic info (ship type, cost) on the list page.
 
 Non-vital development goals, mainly for later development (i.e. out of scope for the coursework):
 
 - As the game designer, I want to add, modify and remove characters and their abilities.
   - Status: Not started
   
 - As game designer or playtester, I want to compare the characteristics of two ships side-by-side.
   - Status: Not started
   
 - As game designer or playtester, I want to see ship statistics in a layout resembling that of the cards in the actual game.
   - Status: Not started
   
 - As the game designer, I want the program to generate images of ship statistics in card form for export
   - Status: Not started
   
# SQL statements

SQL statements relating to the above stories are here in order to not clutter up the user stories themselves. Question marks ('?') in statements are where user input or data retrieved from the database is inserted. (after sanitization by SQLAlchemy)

Adding a ship. Entries are added to the factionship association table according to the factions the user chooses for the ship. (faction_id being the chosen faction, and ship_id the id of the ship that was just added)
```
INSERT INTO ship (name, cost, command_capable, propulsion_type, move, delta_v, evasion_passive, 
evasion_active, evasion_endurance, integrity, primary_facing, armor_front, armor_sides, armor_back)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

INSERT INTO factionship (faction_id, ship_id)
VALUES (?, ?)
```
Updating a ship. Which columns are updated depends on what the user chose to change. Shown here is a statement for including all of them, including removing a faction association and adding another.
```
UPDATE ship SET name=?, cost=?, propulsion_type=?, move=?, delta_v=?, evasion_passive=?, 
evasion_active=?, evasion_endurance=?, integrity=?, primary_facing=?, armor_front=?, 
armor_sides=?, armor_back=?
WHERE ship.id = ?

DELETE FROM factionship WHERE factionship.faction_id = ? AND factionship.ship_id = ?
INSERT INTO factionship (faction_id, ship_id)
```
Removing a ship. Faction associations related to the ship are removed with it. So are its weapons with the weapon removal SQL statement (not duplicated here).
```
DELETE FROM ship WHERE ship.id = ?
DELETE FROM factionship WHERE factionship.ship_id = ?
```
