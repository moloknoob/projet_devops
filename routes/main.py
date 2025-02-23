from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import User, Product
from database.extention import db
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from flask import jsonify
from variables import *
from datetime import timedelta




main_routes = Blueprint('main', __name__)  # Création du Blueprint c'est ce main qu'on utilise dans les URL html par exemple main.home pour rediriger vers l'acceuil
# pour plus de visibilité jai mis l'instance de Blueprint dans une variable main_routes 
@main_routes.route('/')
def home():
    return render_template('index.html')  # Afficher la page d'accueil

@main_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Récupère les données JSON envoyées par React

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"message": "Tous les champs sont requis."}), HTTP_BAD_REQUEST

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "Cet email est déjà utilisé."}), HTTP_BAD_REQUEST

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Inscription réussie !"}), HTTP_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erreur lors de l'inscription : {str(e)}"}), HTTP_INTERNAL_SERVER_ERROR



@main_routes.route('/login', methods=['GET', 'POST']) 
def login():
    if request.method == 'GET':
        return jsonify({"message": "Utilisez une requête POST pour vous connecter."}), HTTP_METHOD_NOT_ALLOWED

    data = request.get_json()
    if not data:
        return jsonify({"message": "Requête invalide, JSON attendu."}), HTTP_UNSUPPORTED_MEDIA_TYPE

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Tous les champs sont requis."}), HTTP_BAD_REQUEST

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Cet email n'existe pas."}), HTTP_UNAUTHORIZED

    if not check_password_hash(user.password, password):
        return jsonify({"message": "Mot de passe incorrect."}), HTTP_UNAUTHORIZED
    expires = timedelta(hours=24)
    token = create_access_token(identity=user.id, expires_delta=expires)
    return jsonify({"message": "Connexion réussie", "token": token, "username": user.username}), HTTP_OK

@main_routes.route('/all_users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    if not users:
        return jsonify({'message': 'No users found'}), HTTP_NOT_FOUND  # Renvoie 404 si aucun utilisateur n'est trouvé
    
    users_list = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
    return jsonify(users_list), HTTP_OK  # Renvoie un statut HTTP_OK pour une requête réussie

@main_routes.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email, 'role': user.role.name}), HTTP_OK 
    else:
        return jsonify({'message': 'Users not found'}), HTTP_NOT_FOUND
    




@main_routes.route('/user_update/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(user_id)
    print(user.id)
    if current_user_id == user_id or user.role.name == 'admin':
        if user:
            data = request.get_json()

            if 'username' in data:
                user.username = data['username']

            if 'email' in data:
                email = data['email']

                existing_user = User.query.filter_by(email=email).first()
                if existing_user and existing_user.email == email:
                    return jsonify({'message': 'email already assigned'}), HTTP_BAD_REQUEST


                user.email = email


            if 'password' in data:
                hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
                user.password = hashed_password
            
                
            db.session.commit()
            return jsonify({'message': 'Users update with succes'}), HTTP_OK 
        else:
            return jsonify({'message': 'Users not found'}), HTTP_NOT_FOUND
    else:
        return jsonify({'message': 'No right to update'}), HTTP_FORBIDDEN


@main_routes.route('/user_delete/<int:user_id>/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id,id):
    current_user_id = get_jwt_identity()
    
    user1 = User.query.get(user_id)
    if current_user_id == user_id or user1.role == "admin":
        user = User.query.get(id)
        if user:
            Product.query.filter_by(user_id=id).delete()
            db.session.delete(user)
            db.session.commit()
            return jsonify({'message': 'Users delete with succes'}), HTTP_OK 
        else:
            return jsonify({'message': 'Users not found'}), HTTP_NOT_FOUND
    else:
        return jsonify({'message': 'No right to update'}), HTTP_FORBIDDEN


@main_routes.route('/all_products', methods=['GET'])
def get_all_products():
    products = Product.query.all()

    # Création de la liste des produits sous forme de dictionnaires
    products_list = [
        {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': float(product.price),  # Conversion Decimal en float si nécessaire
            'stock': product.stock
        }
        for product in products
    ]

    return jsonify(products_list), HTTP_OK


 



@main_routes.route('/order', methods=['GET', 'POST'])
def order():
    return render_template('order.html')

