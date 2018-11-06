from flask import render_template
from application import app

class Item:
    def __init__(self, name):
        self.name = name

nimi = "Essi Esimerkki"

lista = [1, 1, 2, 3, 5, 8, 11]

esineet = []
esineet.append(Item(u"Eka"))
esineet.append(Item(u"Toka"))
esineet.append(Item(u"Kolmas"))
esineet.append(Item(u"Neljäs"))
  
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/demo")
def content():
    return render_template("demo.html", nimi=nimi, lista=lista, esineet=esineet)