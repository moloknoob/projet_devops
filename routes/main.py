from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import User
from database.extention import db


main_routes = Blueprint('main', __name__)  # Création du Blueprint c'est ce main qu'on utilise dans les URL html par exemple main.home pour rediriger vers l'acceuil
# pour plus de visibilité jai mis l'instance de Blueprint dans une variable main_routes 
@main_routes.route('/')
def home():
    return render_template('index.html')  # Afficher la page d'accueil

@main_routes.route('/register', methods=['GET', 'POST'])  
def register():
    if request.method == 'POST':  # ✅ Vérifie si c'est bien un POST
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash("Tous les champs sont requis.", "danger")
            return redirect(url_for('main.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Cet email est déjà utilisé.", "danger")
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Inscription réussie !", "success")
            # return redirect(url_for('main.home'))  # ✅ Redirige après inscription
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur lors de l'inscription : {str(e)}", "danger")

    return render_template('register.html')  

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash("Tous les champs sont requis.", "danger")
            return redirect(url_for('main.login'))

        user = User.query.filter_by(email=email).first()
        if not user:
            flash("Cet email n'existe pas.", "danger")
            return redirect(url_for('main.login'))

        if not check_password_hash(user.password, password):
            flash("Mot de passe incorrect.", "danger")
            return redirect(url_for('main.login'))

        flash("Connexion réussie !", "success")
        return redirect(url_for('main.home'))
    return render_template('login.html')