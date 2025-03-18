from sqlalchemy import Integer, String, Text, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.types import DECIMAL as Decimal
from sqlalchemy.orm import relationship
import enum
from database.extension import db


class UserRole(enum.Enum):
    client = 'client'
    admin = 'admin'

class OrderStatus(enum.Enum):
    panier = 'panier'
    validée = 'validée'
    payée = 'payée'
    expédiée = 'expédiée'
    livrée = 'livrée'
    annulée = 'annulée'

class PaymentStatus(enum.Enum):
    en_attente = 'en attente'
    réussi = 'réussi'
    échec = 'échec'


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(Enum(UserRole), default=UserRole.client)
    created_at = db.Column(TIMESTAMP, default=db.func.current_timestamp())

    orders = relationship('Order', backref='user', lazy=True)

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    name = db.Column(String(255), nullable=False)
    description = db.Column(Text)
    price = db.Column(Decimal(10, 2), nullable=False)
    stock = db.Column(Integer, default=0)
    image = db.Column(db.String(255))
    created_at = db.Column(TIMESTAMP, default=db.func.current_timestamp())

    order_items = relationship('OrderItem', backref='product', lazy=True)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(Decimal(10, 2), nullable=False, default=0)
    status = db.Column(Enum(OrderStatus), default=OrderStatus.panier)
    created_at = db.Column(TIMESTAMP, default=db.func.current_timestamp())

    order_items = relationship('OrderItem', backref='order', lazy=True)
    payment = relationship('Payment', backref='order', uselist=False, lazy=True)

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(Integer, nullable=False)
    price = db.Column(Decimal(10, 2), nullable=False)

class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(Integer, db.ForeignKey('orders.id'), nullable=False)
    payment_method = db.Column(Enum('carte', 'paypal', 'virement'), nullable=False)
    payment_status = db.Column(Enum(PaymentStatus), default=PaymentStatus.en_attente)
    created_at = db.Column(TIMESTAMP, default=db.func.current_timestamp())


 


class Cart(db.Model):
    __tablename__ = 'cart'  # Nom de la table dans la base de données

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Identifiant du panier
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Clé étrangère vers la table Users
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)  # Clé étrangère vers la table Products
    quantity = db.Column(db.Integer, nullable=False)  # Quantité du produit dans le panier
    created_at = db.Column(TIMESTAMP, default=db.func.current_timestamp())  # Date de création du panier

    # Définition des relations
    user = db.relationship('User', backref='cart_items', lazy=True)
    product = db.relationship('Product', backref='cart_items', lazy=True)
    # Constructeur
    def __init__(self, user_id, product_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
    # Méthode d'affichage pour debuguer
    def __repr__(self):
        return f"<Cart {self.id} - User {self.user_id} - Product {self.product_id}>"
