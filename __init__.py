from flask import Flask, send_from_directory, render_template
from database.extention import db  # Importer SQLAlchemy
from variables import DATABASE_URL,SECRET_KEY  # Importer la config de la base de données
import logging # c'est pour debug, ca remplace un peu print 
from routes.main import main_routes # Importer les routes
from sqlalchemy import text 

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Config BDD
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY  # Clé secrète pour les sessions si je met pas sa je peux pas utiliser flash qui est utile pour les session et pour les msg dans le html

    # Init on initialise la base de données pour l'instance app
    db.init_app(app)

    with app.app_context():
        try:
            result = db.session.execute(text('show databases;'))  # Utilisation de text()
            print("Connexion à la base de données réussie.")
            print(result.fetchall())
        except Exception as e:
            logging.error(f'Erreur de connexion à la base de données : {str(e)}')
            print(f'Erreur de connexion à la base de données : {str(e)}')
            
     # on enregistre les route ici grace aux blueprints, je decouperais les routes plus tard pour une meilleur organisation main, auth, admin etc
    app.register_blueprint(main_routes)
   
    return app
