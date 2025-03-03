import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from __init__ import create_app

app = create_app()  # on apelle create_app() pour creer recuperer l'instantiation de l'application et la mettre dans app

# il est important de crée ce fichier et lancer le serveur via ce fichier run.py , on initialise le serveur ici et on instancie dans lautre fichier
if __name__ == "__main__":
    app.run(debug=True)
