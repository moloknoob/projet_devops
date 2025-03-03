from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import User, Product, Order, OrderItem,Cart
from database.extention import db
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from variables import *
from datetime import timedelta

main_routes = Blueprint('main', __name__)

# 🔹 Route d'accueil
@main_routes.route('/')
def home():
    return jsonify({"message": "Bienvenue sur mon site"}), HTTP_OK

# 🔹 Inscription d'un utilisateur
@main_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username, email, password = data.get("username"), data.get("email"), data.get("password")

    if not all([username, email, password]):
        return jsonify({"message": "Tous les champs sont requis."}), HTTP_BAD_REQUEST

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Cet email est déjà utilisé."}), HTTP_BAD_REQUEST

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "Inscription réussie !"}), HTTP_CREATED
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Erreur : {str(e)}"}), HTTP_INTERNAL_SERVER_ERROR

# 🔹 Connexion d'un utilisateur
@main_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email, password = data.get("email"), data.get("password")

    if not all([email, password]):
        return jsonify({"message": "Tous les champs sont requis."}), HTTP_BAD_REQUEST

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"message": "Email ou mot de passe incorrect."}), HTTP_UNAUTHORIZED

    token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))
    return jsonify({"message": "Connexion réussie", "token": token, "username": user.username}), HTTP_OK

# 🔹 Récupération de tous les utilisateurs
@main_routes.route('/all_users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    if not users:
        return jsonify({"message": "Aucun utilisateur trouvé."}), HTTP_NOT_FOUND

    return jsonify([{"id": u.id, "username": u.username, "email": u.email} for u in users]), HTTP_OK

# 🔹 Récupération des infos d'un utilisateur
@main_routes.route('/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    return jsonify({
        "id": user.id, "username": user.username, "email": user.email, "role": user.role.name
    }) if user else (jsonify({"message": "Utilisateur non trouvé."}), HTTP_NOT_FOUND)

# 🔹 Mise à jour des infos d'un utilisateur
@main_routes.route('/user_update/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "Utilisateur non trouvé."}), HTTP_NOT_FOUND

    if current_user_id != user_id and user.role.name != 'admin':
        return jsonify({"message": "Non autorisé."}), HTTP_FORBIDDEN

    data = request.get_json()
    if "username" in data:
        user.username = data["username"]

    if "email" in data:
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"message": "Email déjà utilisé."}), HTTP_BAD_REQUEST
        user.email = data["email"]

    if "password" in data:
        user.password = generate_password_hash(data["password"])

    db.session.commit()
    return jsonify({"message": "Utilisateur mis à jour avec succès."}), HTTP_OK

# 🔹 Suppression d'un utilisateur
@main_routes.route('/user_delete/<int:user_id>/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id, id):
    current_user_id = get_jwt_identity()
    user = User.query.get(id)

    if not user:
        return jsonify({"message": "Utilisateur non trouvé."}), HTTP_NOT_FOUND

    if current_user_id != user_id and user.role.name != "admin":
        return jsonify({"message": "Non autorisé."}), HTTP_FORBIDDEN

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Utilisateur supprimé avec succès."}), HTTP_OK

# 🔹 Récupération de tous les produits
@main_routes.route('/all_products', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    if not products:
        return jsonify({"message": "Aucun produit trouvé."}), HTTP_NOT_FOUND

    return jsonify([
        {
            "id": p.id, "name": p.name, "price": p.price, 
            "stock": p.stock if p.stock > 0 else "Rupture de stock",
            "image": p.image
        } for p in products
    ]), HTTP_OK

# 🔹 Gestion des commandes d'un utilisateur
@main_routes.route('/order', methods=['GET', 'POST'])
@jwt_required()
def order():
    user_id = get_jwt_identity()

    if request.method == 'GET':
        orders = Order.query.filter_by(user_id=user_id).all()
        if not orders:
            return jsonify({"message": "Aucune commande trouvée."}), HTTP_NOT_FOUND

        return jsonify([
            {
                "id": o.id, "total_price": float(o.total_price),
                "status": o.status.name, "created_at": o.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "items": [{"product_id": i.product_id, "quantity": i.quantity, "price": float(i.price)} for i in o.order_items]
            } for o in orders
        ]), HTTP_OK

    elif request.method == 'POST':
        data = request.get_json()
        if not data or "items" not in data:
            return jsonify({"message": "Données invalides."}), HTTP_BAD_REQUEST

        new_order = Order(user_id=user_id, total_price=0)
        db.session.add(new_order)
        db.session.flush()

        total_price = sum(item["quantity"] * item["price"] for item in data["items"])
        order_items = [OrderItem(order_id=new_order.id, product_id=item["product_id"], quantity=item["quantity"], price=item["price"]) for item in data["items"]]

        new_order.total_price = total_price
        db.session.add_all(order_items)
        db.session.commit()

        return jsonify({"message": "Commande créée avec succès", "order_id": new_order.id}), HTTP_CREATED

@main_routes.route('/validate-cart', methods=['POST'])
def validate_cart():
    try:
        data = request.json  # On reçoit les données au format JSON depuis le frontend
        user_id = data.get('user_id')  # ID de l'utilisateur
        products = data.get('products')  # Liste des produits du panier
        total_price = data.get('total_price')  # Prix total de la commande

        # Vérification des données reçues
        if not user_id or not products or not total_price:
            return jsonify({"error": "Données manquantes"}), 400

        # Pour chaque produit dans le panier, créer un élément Cart correspondant
        for product in products:
            product_id = product.get('id')
            quantity = product.get('quantity')

            if not product_id or not quantity:
                return jsonify({"error": "Produit incomplet"}), 400

            # Créer un élément de panier pour chaque produit
            new_cart_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)

            # Ajouter le nouvel élément de panier dans la session
            db.session.add(new_cart_item)

        # Commit des changements dans la base de données
        db.session.commit()

        return jsonify({"message": "Commande validée avec succès", "total_price": total_price}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500