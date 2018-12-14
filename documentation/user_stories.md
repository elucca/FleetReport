# User stories

- As the game designer, I require an admin account with full access to modifying data.
  - Status: Implemented
  
- As the game designer, I want to add, modify and remove ships.
  - Status: Implemented

- As the game designer, I want to add weapons to a ship, and to modify and remove them
  - Status: Implemented. Laser and ewar data types are 'stubs' in that they don't contain all the data required for the game. This will be rectified later. (out of scope for coursework)

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

## Adding, removing and updating ships

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

## Adding, removing and updating weapons

Shown here are statements relating to the CIWS weapon type. The statements for other weapon types are very directly analogous.

Adding a weapon. A weapon is always related to a particular ship, so the ship's id must be provided as a foreign key.
```
INSERT INTO "CIWS" (name, dmg_missile, dmg_ship, ship_id)
VALUES (?, ?, ?, ?)
```
Updating a weapon. Only those columns the user actually updated are included in the statement.
```
UPDATE "CIWS" SET name=?, dmg_missile=?, dmg_ship=?
WHERE "CIWS".id = ?
```
Removing a weapon. This statement is used both when the user directly removes a weapon, and when a user removes a ship, which will cause its weapons to also be removed.
```
DELETE FROM "CIWS" WHERE "CIWS".id = ?
```

## Adding, removing and updating factions

Adding a faction.
```
INSERT INTO faction (name)
VALUES (?)
```

Updating a faction.
```
UPDATE faction SET name=?
WHERE faction.id = ?
```

Removing a faction. Removing a faction does not cause its associated ships to be removed, but will remove association table entries.
```
DELETE FROM faction WHERE faction.id = ?
DELETE FROM factionship WHERE factionship.faction_id = ?
```

## Inspecting a ship

Viewing a ship's characteristics retrieves the ship itself, any associated factions, and any associated weapons. All weapon tables are queried, but for brevity shown here is only the query for the CIWS table, as the rest are very similar.
```
SELECT ship.id AS ship_id, ship.name AS ship_name, ship.cost AS ship_cost, ship.command_capable 
AS ship_command_capable, ship.propulsion_type AS ship_propulsion_type, ship.move AS ship_move, 
ship.delta_v AS ship_delta_v, ship.evasion_passive AS ship_evasion_passive, ship.evasion_active 
AS ship_evasion_active, ship.evasion_endurance AS ship_evasion_endurance, ship.integrity AS 
ship_integrity, ship.primary_facing AS ship_primary_facing, ship.armor_front AS ship_armor_front, 
ship.armor_sides AS ship_armor_sides, ship.armor_back AS ship_armor_back
FROM ship
WHERE ship.id = ?

SELECT faction.id AS faction_id, faction.name AS faction_name
FROM faction, factionship
WHERE ? = factionship.ship_id AND faction.id = factionship.faction_id

SELECT "CIWS".id AS "CIWS_id", "CIWS".name AS "CIWS_name", "CIWS".dmg_missile AS "CIWS_dmg_missile", 
"CIWS".dmg_ship AS "CIWS_dmg_ship", "CIWS".ship_id AS "CIWS_ship_id"
FROM "CIWS"
WHERE ? = "CIWS".ship_id
```

## Listing all ships

Ships are displayed in a list per-faction, including a category for ships with no faction. Thus all ships and all factions are retrieved from the database.

```
SELECT faction.id AS faction_id, faction.name AS faction_name
FROM faction

SELECT ship.id AS ship_id, ship.name AS ship_name, ship.cost AS ship_cost, ship.command_capable 
AS ship_command_capable, ship.propulsion_type AS ship_propulsion_type, ship.move AS ship_move, 
ship.delta_v AS ship_delta_v, ship.evasion_passive AS ship_evasion_passive, ship.evasion_active 
AS ship_evasion_active, ship.evasion_endurance AS ship_evasion_endurance, ship.integrity AS 
ship_integrity, ship.primary_facing AS ship_primary_facing, ship.armor_front AS 
ship_armor_front, ship.armor_sides AS ship_armor_sides, ship.armor_back AS ship_armor_back
FROM ship, factionship
WHERE ? = factionship.faction_id AND ship.id = factionship.ship_id
```
