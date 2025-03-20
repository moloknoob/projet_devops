from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import User, Product, Order, OrderItem,Cart, PaymentStatus, OrderStatus, Payment
from database.extension import db
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity
)
from variables import *
from datetime import timedelta
from sqlalchemy.orm import joinedload
 

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
    


@main_routes.route('/cart/<int:item_id>', methods=['PUT'])
def update_quantity(item_id):
    try:
        data = request.get_json()
        quantity = data.get('quantity')

        if quantity is None or quantity < 1:
            return jsonify({"error": "La quantité doit être supérieure ou égale à 1."}), 400

        item = Cart.query.get(item_id)

        if item is None:
            return jsonify({"error": "L'élément n'existe pas dans le panier."}), 404

        item.quantity = quantity
        db.session.commit()

        return jsonify({"message": "Quantité mise à jour."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Supprimer un produit du panier
@main_routes.route('/cart/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    try:
        item = Cart.query.get(item_id)

        if item is None:
            return jsonify({"error": "L'élément n'existe pas dans le panier."}), 404

        db.session.delete(item)
        db.session.commit()

        return jsonify({"message": "Produit supprimé du panier."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
 
    


@main_routes.route('/cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()

        user_id = data.get('user_id')
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        # Vérifier si le produit est déjà dans le panier
        existing_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

        if existing_item:
            # Si le produit est déjà dans le panier, on met à jour la quantité
            existing_item.quantity += quantity
            db.session.commit()
            return jsonify({"message": "Quantité mise à jour dans le panier."}), 200
        else:
            # Sinon, on ajoute un nouvel article au panier
            new_item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
            db.session.add(new_item)
            db.session.commit()
            return jsonify({"message": "Produit ajouté au panier."}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@main_routes.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    try:
        # Récupérer les articles du panier pour un utilisateur donné
        cart_items = Cart.query.filter_by(user_id=user_id).options(joinedload(Cart.product)).all()

        # Renvoyer une liste vide au lieu d'une erreur si le panier est vide
        if not cart_items:
            return jsonify([]), 200  

        # Construire la réponse JSON
        cart_data = [
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product.name,
                "product_description": item.product.description,
                "product_price": item.product.price,
                "quantity": item.quantity,
                "total_price": item.product.price * item.quantity,
                "image": item.product.image
            }
            for item in cart_items
        ]

        return jsonify(cart_data), 200
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # Log détaillé de l'erreur
        return jsonify({"error": str(e)}), 500
    


# 🔹 Créer une commande à partir du panier
def create_order(user_id):
    try:
        cart_items = Cart.query.filter_by(user_id=user_id).all()
        if not cart_items:
            return jsonify({"message": "Le panier est vide."}), 400

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        new_order = Order(user_id=user_id, total_price=total_price, status=OrderStatus.en_cours)
        db.session.add(new_order)
        db.session.flush()

        for item in cart_items:
            order_item = OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity, price=item.product.price)
            db.session.add(order_item)
            
            # Mise à jour du stock produit
            product = Product.query.get(item.product_id)
            if product.stock < item.quantity:
                return jsonify({"message": f"Stock insuffisant pour {product.name}."}), 400
            product.stock -= item.quantity
            
        db.session.commit()
        return jsonify({"message": "Commande créée avec succès", "order_id": new_order.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 🔹 Effectuer un paiement pour une commande
@main_routes.route('/pay-order', methods=['POST'])
def pay_order():
    try:
        data = request.get_json()
        order_id = data.get("order_id")
        payment_method = data.get("payment_method")

        order = Order.query.get(order_id)
        if not order:
            return jsonify({"message": "Commande non trouvée."}), 404
        
        if order.payment:
            return jsonify({"message": "Commande déjà payée."}), 400
        
        new_payment = Payment(order_id=order.id, payment_method=payment_method, payment_status=PaymentStatus.confirme)
        order.status = OrderStatus.paye
        
        db.session.add(new_payment)
        db.session.commit()

        return jsonify({"message": "Paiement effectué avec succès"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# 🔹 Récupérer l'historique des paiements d'un utilisateur
@main_routes.route('/payments/<int:user_id>', methods=['GET'])
def get_payments(user_id):
    try:
        orders = Order.query.filter_by(user_id=user_id).options(joinedload(Order.payment)).all()
        payments = []
        
        for order in orders:
            if order.payment:
                payments.append({
                    "order_id": order.id,
                    "total_price": order.total_price,
                    "payment_method": order.payment.payment_method,
                    "payment_status": order.payment.payment_status.name,
                    "created_at": order.payment.created_at
                })
        
        return jsonify(payments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@main_routes.route('/create-order', methods=['POST'])
def create_order_route():
    data = request.get_json()
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"message": "User ID requis."}), HTTP_BAD_REQUEST

    try:
        # Récupérer les articles du panier pour l'utilisateur avec les infos produit
        cart_items = Cart.query.filter_by(user_id=user_id).options(joinedload(Cart.product)).all()
        if not cart_items:
            return jsonify({"message": "Le panier est vide."}), 400

        # Calcul du prix total en utilisant les infos du produit
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        
        # Créer une nouvelle commande avec le statut "en_cours"
        new_order = Order(user_id=user_id, total_price=total_price, status=OrderStatus.en_cours)
        db.session.add(new_order)
        db.session.flush()  # Permet d'obtenir l'ID de la commande créée

        # Pour chaque article du panier, créer un OrderItem et mettre à jour le stock du produit
        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.product.price
            )
            db.session.add(order_item)
            
            # Récupérer le produit pour vérifier et mettre à jour le stock
            product = Product.query.get(item.product_id)
            if product.stock < item.quantity:
                db.session.rollback()
                return jsonify({"message": f"Stock insuffisant pour {product.name}."}), 400
            product.stock -= item.quantity
        
        db.session.commit()
        return jsonify({"message": "Commande créée avec succès", "order_id": new_order.id}), HTTP_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_INTERNAL_SERVER_ERROR
