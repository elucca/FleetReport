# FleetReport
A game design tool for storing data for an as-yet unnamed space wargame

## Description

FleetReport is a web-based app for aiding in the design of a tactical space wargame design I'm working on, which I may eventually implement in both video game and boardgame form. The intent of FleetReport is to store and handle data related to this game and its mechanics - in particular, the statistics and other data of factions, characters, special abilities, ships and weapons. FleetReport will store these entries in a nice and centralized form from which they can be retrieved for the actual game implementations. It will also aid in designing and balancing the game and provide a useful reference for both me and playtesters.

## Planned core features

- Account and login system - admin can see and modify data, guests can see it
- Adding, modifying and removing faction, character, ability, ship and weapon entries
- Recording of game version and balancing changes related to the above
- UI for displaying entries (incl. collecting related entries, for example accessing a ship should also display its weapons), by faction and possibly other criteria
- Analysis of entries to aid in balancing - for instance, how many points does the average ship cost for Faction A, or how do two ships compare in stats and cost

## Stretch goals:
- Ability to output each type of entry into some human-readable file format for video game use
- Ability to output entries into card images for boardgame use
