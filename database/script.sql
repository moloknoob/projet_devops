-- Création de la base de données si elle n'existe pas
CREATE DATABASE IF NOT EXISTS anime;
USE anime;

-- Table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('client', 'admin') DEFAULT 'client',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Afficher toutes les tables
SHOW TABLES;


-- script.sql

-- Insérer un produit seulement s'il n'existe pas déjà
INSERT INTO products (name, description, price, stock)
SELECT 'Escanor', 'L''humain au panthéon des races', 49.99, 20
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'Escanor');

INSERT INTO products (name, description, price, stock)
SELECT 'Guts', 'Le berserker ultime', 59.99, 20
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'Guts');

INSERT INTO products (name, description, price, stock)
SELECT 'Ken', 'Le survivant de l''enfer', 79.99, 20
WHERE NOT EXISTS (SELECT 1 FROM products WHERE name = 'Ken');

UPDATE users
SET role = 'admin'
WHERE id = 11;



INSERT INTO products (name, description, price, stock) VALUES
('Escanor', 'Le Lion de l\'Orgueil - Un guerrier surpuissant.', 49.99, 10),
('Guts', 'Le légendaire épéiste du manga Berserk.', 59.99, 8),
('Ken', 'Le maître du Hokuto Shinken.', 39.99, 12);


ALTER TABLE products ADD COLUMN image VARCHAR(255);

INSERT INTO products (name, description, price, stock, image) VALUES
('Escanor', 'Le Lion de l\'Orgueil - Un guerrier surpuissant.', 49.99, 10, 'static/img/escanor.jpg'),
('Guts', 'Le légendaire épéiste du manga Berserk.', 59.99, 8, 'static/img/Guts.webp'),
('Ken', 'Le maître du Hokuto Shinken.', 39.99, 12, 'static/img/Ken.jpg');
-- Création de la table Cart
CREATE TABLE IF NOT EXISTS cart (
    id INT AUTO_INCREMENT PRIMARY KEY,      -- Identifiant unique pour chaque entrée
    user_id INT NOT NULL,                   -- Référence à l'utilisateur qui a ajouté un produit
    product_id INT NOT NULL,                -- Référence au produit ajouté au panier
    quantity INT NOT NULL,                  -- Quantité du produit dans le panier
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Date et heure d'ajout au panier
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE, -- Clé étrangère vers la table users
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE -- Clé étrangère vers la table products
);
