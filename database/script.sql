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