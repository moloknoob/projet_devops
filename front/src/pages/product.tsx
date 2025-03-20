import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/product.css";

interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  image: string;
}

interface CartItem extends Product {
  quantity: number;
}

const Product = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [cart, setCart] = useState<CartItem[]>(() => {
    const savedCart = localStorage.getItem("cart");
    return savedCart ? JSON.parse(savedCart) : [];
  });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  // 🔹 Récupération des produits depuis le backend
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await fetch("http://localhost:5000/all_products");

        if (!response.ok) {
          throw new Error("Erreur lors du chargement des produits.");
        }

        const data = await response.json();
        setProducts(data);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  // 🔹 Ajouter un produit au panier avec gestion de quantité
  const addToCart = (product: Product) => {
    const existingItem = cart.find((item) => item.id === product.id);

    if (existingItem) {
      setMessage(`${product.name} est déjà dans le panier.`);
      setTimeout(() => setMessage(""), 2000);
      return;
    }

    if (product.stock > 0) {
      const newCart = [...cart, { ...product, quantity: 1 }];
      setCart(newCart);
      localStorage.setItem("cart", JSON.stringify(newCart));
      setMessage(`${product.name} ajouté au panier !`);
      setTimeout(() => setMessage(""), 2000);
    } else {
      setMessage(`${product.name} est en rupture de stock.`);
      setTimeout(() => setMessage(""), 2000);
    }
  };

  const updateQuantity = (productId: number, delta: number) => {
    const updatedCart = cart.map((item) => {
      if (item.id === productId) {
        const newQuantity = item.quantity + delta;
        if (newQuantity > item.stock) {
          setMessage(`Stock insuffisant pour ${item.name}.`);
          setTimeout(() => setMessage(""), 2000);
          return item;
        }
        return { ...item, quantity: Math.max(1, newQuantity) };
      }
      return item;
    });
    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  };
  // 🔹 Supprimer un produit du panier
  const removeFromCart = (productId: number) => {
    const updatedCart = cart.filter((item) => item.id !== productId);
    setCart(updatedCart);
    localStorage.setItem("cart", JSON.stringify(updatedCart));
  };

  // 🔹 Valider le panier et l'envoyer au backend
  const handleValidateCart = async () => {
    if (cart.length === 0) {
      alert("Votre panier est vide !");
      return;
    }

    if (!token) {
      alert("Veuillez vous connecter pour valider la commande.");
      return;
    }

    try {
      // Extraction de l'ID utilisateur depuis le token
      const decodedToken = JSON.parse(atob(token.split(".")[1])); // Décoder le payload du token JWT
      const userId = decodedToken.sub; // Utiliser 'sub' pour l'ID utilisateur
      console.log("Token:", decodedToken);
      console.log("User ID:", userId);
      // Structure des données à envoyer au backend
      const orderData = {
        user_id: userId, // ID de l'utilisateur extrait du token
        products: cart.map((item) => ({
          id: item.id,
          name: item.name,
          price: item.price,
          quantity: item.quantity,
        })),
        total_price: cart.reduce(
          (total, item) => total + item.price * item.quantity,
          0
        ),
      };

      // Envoi de la commande au backend
      const response = await fetch("http://localhost:5000/validate-cart", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(orderData),
      });

      if (!response.ok) {
        throw new Error("Erreur lors de la validation du panier.");
      }

      const result = await response.json();
      alert("Panier validé avec succès !");
      console.log(result); // Afficher la réponse du backend

      // Vider le panier après validation
      setCart([]);
      localStorage.removeItem("cart");
    } catch (error) {
      console.error(error);
      alert("Une erreur est survenue lors de la validation du panier.");
    }
  };

  // 🔹 Affichage du message d'erreur ou de chargement
  if (loading) return <p>Chargement des produits...</p>;
  if (error) return <p className="error-message">{error}</p>;

  return (
    <div className="product-container">
      <h2 className="product-title">Nos Produits</h2>
      {message && <p className="message">{message}</p>}

      <div className="product-list">
        {products.map((product) => (
          <div key={product.id} className="product-card">
            <img
              src={`http://localhost:5000/${product.image}`} // Prendre en compte le chemin relatif complet
              alt={product.name}
              className="product-image"
            />
            <h3>{product.name}</h3>
            <p className="product-description">{product.description}</p>{" "}
            {/* Description sous le nom */}
            <p className="product-price">
              {product.price ? product.price + " €" : "Prix non disponible"}
            </p>
            <p className="product-stock">
              {product.stock > 0
                ? `Stock: ${product.stock}`
                : "Rupture de stock"}
            </p>
            <button
              className="buy-button"
              onClick={() => addToCart(product)}
              disabled={product.stock === 0}
            >
              {product.stock > 0 ? "Ajouter au panier" : "Indisponible"}
            </button>
          </div>
        ))}
      </div>

      {/* 🔹 Affichage du panier */}
      {cart.length > 0 && (
        <div className="cart">
          <h3>🛒 Votre Panier</h3>
          {cart.map((item) => (
            <div key={item.id} className="cart-item">
              <span>
                {item.name} x{item.quantity}
              </span>
              <button onClick={() => updateQuantity(item.id, -1)}>-</button>
              <button onClick={() => updateQuantity(item.id, 1)}>+</button>
              <button
                className="remove-button"
                onClick={() => removeFromCart(item.id)}
              >
                X
              </button>
            </div>
          ))}

          {/* 🔹 Afficher le bouton de validation du panier */}
          <button className="validate-cart-button" onClick={handleValidateCart}>
            Valider mon panier
          </button>
        </div>
      )}

      <button
        className="cart-button"
        onClick={() => navigate("/cart", { state: { cart } })}
      >
        Voir mon panier
      </button>
    </div>
  );
};

export default Product;
