# FleetReport

The app's current development build can be accessed at https://fleetreport.herokuapp.com/. For full access for testing purposes, you can log in with the username 'admin' and password 'admin'. This is the only user which now has access to editing data. Feel free to experiment.

## Description

FleetReport is a web-based app for aiding in the design of a tactical space wargame design I'm working on, which I may eventually implement in both video game and boardgame form. The intent of FleetReport is to store and handle data related to this game and its mechanics - in particular, the statistics and other data of factions, characters, special abilities, ships and weapons. FleetReport will store these entries in a nice and centralized form from which they can be retrieved for the actual game implementations. It will also aid in designing and balancing the game and provide a useful reference for both me and playtesters. The initial implementation will focus on ships and their weapons, with factions, characters and their abilities planned to be added later.

## Documentation
[User manual](https://github.com/elucca/FleetReport/blob/master/documentation/User_manual.md)

[User stories](https://github.com/elucca/FleetReport/blob/master/documentation/user_stories.md)

[Database diagram](https://raw.githubusercontent.com/elucca/FleetReport/master/documentation/FleetReport_db.png)

## Planned core features

- Account and login system - anyone can see the entries, but only admins can alter them
- Adding, modifying and removing ship and weapon entries
- UI for displaying entries (incl. collecting related entries, for example accessing a ship should also display its weapons), by faction and possibly other criteria
- Analysis of entries to aid in balancing - for instance, how many points does the average ship cost, or how do two ships compare in stats and cost

## Stretch goals:
- Adding, modifying and removing faction, character and ability entries
- Recording of old versions of entries
- Ability to output each type of entry into some human-readable file format for video game use
- Ability to output entries into card images for boardgame use
