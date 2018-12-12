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

3. Install the program's dependencies. These will be installed to the virtual environment contained in the program's folder.
On Linux and Windows:

```
pip install -r requirements.txt
```

4. Run the program:

On Linux:
```
python3 run.py
```

On Windows:
```
python run.py
```

5. Access the program through a web browser by navigating to the address:
```
http://localhost:5000
```

### A note on local vs online versions
When ran locally, the database is contained inside the program folder on your computer, and will initially be empty. When using the online version, the database is located on the server and is common to all users. During the development period, full access to both is provided by the username 'admin' and 'password' admin. When the program reaches release, admin access to the online version will be restricted.

### Deploying on Heroku
You can also make your own online deployment of the app on Heroku. To do this you'll need a Heroku account and [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli). Follow the instructions on Heroku's page.

From the command line, after installing Heroku CLI:

1. Fork the repository on GitHUb.

3. Clone your fork of the repository to your computer and navigate to its folder using the command line. Install its dependencies with:
```
pip install -r requirements.txt
```

2. Create your own deployment of the app on Heroku with:
```
heroku create <unique name for your deployment>
```

4. On the last step, you should see the address https://git.heroku.com/Add/<unique name of your deployment>.git. Add this as a remote repository to your version control with:
```
git remote add heroku https://git.heroku.com/<unique name of your deployment>.git
```

5. Finally, push to the Heroku repository:
```
git push heroku master
```

You now have your own online deployment of the app which you have full access to using Heroku's command line tools and online dashboard. You can also set it to track commits to your forked repository by following the instructions [here](https://devcenter.heroku.com/articles/github-integration).


## Usage

Note: The program is related to a game, and this document focuses on explaining purely the usage of this program and not the rules of the game. Thus the meaning of particular ship statistics and the like may not be readily apparent, and will be explained elsewhere. (out of the scope of this project as coursework)

The program is navigated using the nav bar at the top of the screen. The navbar is intended to have direct links to the most common operations: Viewing factions, viewing ships, adding ships, logging in and registering. In the future, a link to a character page will be added.

As a non-admin user, you can view all factions and ships on their respective pages. Since a ship has quite a lot of information, the list page displays only their names, which are links to a page which contains their full info sheet.

Options related to modifying data (for instance, adding ships) are only available when logged in with an admin account, and are not otherwise visible in the user interface. While the program is under development, you can gain admin access by logging in with the username 'admin' and password 'admin'.

With admin access, you can add new ships and factions. In addition, you can modify and remove them. For factions, these options are available directly on the list page, and for ships on a given ship's info page. A ship's modification page also allows adding any type of weapon to the ship, which will subsequently be displayed on its info sheet.

A note on removing data: When removing a faction, ships belonging to that faction will remain, but their association to the faction will be lost. Should a ship not belong to any faction, it will be listed under 'Ships belonging to no faction' on the ships page.
On the other hand, when removing a ship, all of its weapons will be removed with it as each weapon is unique to a ship

