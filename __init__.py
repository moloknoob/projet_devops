from flask import Flask
from database.extension import db  # Importer SQLAlchemy
from variables import DATABASE_URL,SECRET_KEY  # Importer la config de la base de données 
from routes.main import main_routes # Importer les routes
from sqlalchemy import text 
from flask_jwt_extended import  JWTManager
from flask_cors import CORS
import logging 


  

def create_app():
    app = Flask(__name__, static_folder='static')

    # Config BDD
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = SECRET_KEY  

    # Init on initialise la base de données pour l'instance app
    db.init_app(app)

    with app.app_context():
        try:
            result = db.session.execute(text('show databases;'))  # Utilisation de text() sinon ce n'est pas considerer comme du texte
            print("Connexion à la base de données réussie.")
            print(result.fetchall())
        except Exception as e:
            logging.error(f'Erreur de connexion à la base de données : {str(e)}')
            print(f'Erreur de connexion à la base de données : {str(e)}')
            
     # on enregistre les route ici grace aux blueprints, je decouperais les routes plus tard pour une meilleur organisation main, auth, admin etc
    app.register_blueprint(main_routes)
    app.config["JWT_SECRET_KEY"] = "2165165156165161"
    jwt = JWTManager(app)
    CORS(app)   
     
     

   
    return app


