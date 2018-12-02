# User manual

## Acquiring and running the program

The easiest way to use the program is to access its online version at https://fleetreport.herokuapp.com/.

The program can also be ran locally, though doing this is a bit more involved, and only necessary if you are interested in testing or investigating it in a more thorough way. You will need to have Python installed. The steps to running the program locally are as follows.
1. Download the repository to your computer.
2. Open a command prompt, and first activate the virtual environment:

On Linux:
First navigate to the program's main folder. (which contains run.py)
```
source venv/bin/activate
```

On Windows:
```
<path to FleetReport folder>\venv\Scripts\activate
```

3. Run the program:

On Linux:
```
python3 run.py
```

On Windows:
```
python run.py
```

4. Access the program through a web browser by navigating to the address:
```
http://localhost:5000
```

### A note on local vs online versions
When ran locally, the database is contained inside the program folder on your computer, and will initially be empty. When using the online version, the database is located on the server and is common to all users. During the development period, full access to both is provided by the username 'admin' and 'password' admin. When the program reaches release, admin access to the online version will be restricted.

## Usage

The program is navigated using the nav bar at the top of the screen. The UI strives to be self-explanatory, but at this point it's still very much a work in progress. Features will become available gradually, and everything about the UI is subject to change. A proper user manual may be provided when the program is more complete and well-defined.

Some preliminary notes on the currently less self-explanatory aspects:
- Weapons can be added on the ship modification page. Both ships and weapons can be removed on their respective modification pages.
- Removing a ship will remove all its weapons.
- Removing a faction will *not* remove any ships, but will remove any association a ship has with the deleted faction. Should a ship lose all of its factions, it will be placed in the "Ships with no faction" category on the list page.


