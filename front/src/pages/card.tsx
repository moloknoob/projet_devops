import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

// Interface pour décrire un élément du panier avec les informations du produit
interface CartItem {
  id: number;
  product_id: number;
  product_name: string;
  product_description: string;
  product_price: number;
  quantity: number;
  total_price: number;
  image: string;
}

const Cart = () => {
  const [cart, setCart] = useState<CartItem[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  // Récupérer le panier de l'utilisateur
  useEffect(() => {
    const fetchCart = async () => {
      try {
        if (!token) {
          throw new Error("Veuillez vous connecter pour voir votre panier.");
        }

        // Décoder le token pour récupérer l'ID de l'utilisateur
        const decodedToken = JSON.parse(atob(token.split(".")[1])); // Décoder le payload du token JWT
        const userId = decodedToken.sub; // ID de l'utilisateur dans le token

        const response = await fetch(`http://localhost:5000/cart/${userId}`);
        if (!response.ok) {
          throw new Error("Erreur lors du chargement du panier.");
        }
        const data = await response.json();
        console.log(data);
        setCart(data); // Mettre à jour l'état du panier
      } catch (err: any) {
        setError(err.message); // En cas d'erreur
      } finally {
        setLoading(false); // Fin du chargement
      }
    };

    fetchCart();
  }, [token]);

  // Mettre à jour la quantité du produit dans le panier
  const updateQuantity = async (productId: number, delta: number) => {
    const updatedCart = cart.map((item) =>
      item.id === productId
        ? {
            ...item,
            quantity: Math.max(1, item.quantity + delta), // Empêcher d'avoir une quantité inférieure à 1
            total_price: item.product_price * (item.quantity + delta), // Calculer le nouveau prix total
          }
        : item
    );
    setCart(updatedCart); // Mettre à jour le panier localement

    // Mettre à jour la quantité dans la base de données
    const updatedItem = updatedCart.find((item) => item.id === productId);
    if (updatedItem) {
      await updateCartInDB(updatedItem);
    }
  };

  // Supprimer un produit du panier
  const removeFromCart = async (productId: number) => {
    const updatedCart = cart.filter((item) => item.id !== productId);
    setCart(updatedCart);

    // Supprimer le produit dans la base de données
    await deleteFromCartDB(productId);
  };

  // Mettre à jour le panier dans la base de données
  const updateCartInDB = async (item: CartItem) => {
    try {
      const response = await fetch(`http://localhost:5000/cart/${item.id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ quantity: item.quantity }),
      });

      if (!response.ok) {
        throw new Error("Erreur lors de la mise à jour du panier.");
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  // Supprimer un produit du panier dans la base de données
  const deleteFromCartDB = async (productId: number) => {
    try {
      const response = await fetch(`http://localhost:5000/cart/${productId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error("Erreur lors de la suppression du produit du panier.");
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  // Affichage du panier
  if (loading) return <p>Chargement de votre panier...</p>;
  if (error) return <p className="error-message">{error}</p>;

  return (
    <div className="cart-container">
      <h2>🛒 Votre Panier</h2>
      {cart.length === 0 ? (
        <p>Votre panier est vide.</p>
      ) : (
        <div className="cart-items">
          {cart.map((item) => (
            <div key={item.id} className="cart-item">
              <img
                src={`http://localhost:5000/${item.image}`} // Affichage de l'image du produit
                alt={item.product_name}
                className="cart-item-image"
              />
              <div className="cart-item-details">
                <h3>{item.product_name}</h3>
                <p>{item.product_description}</p>
                <p>Prix : {item.product_price} €</p>
                <p>Total : {item.total_price} €</p>
                <div className="quantity-controls">
                  <button onClick={() => updateQuantity(item.id, -1)}>-</button>
                  <span>Quantité : {item.quantity}</span>
                  <button onClick={() => updateQuantity(item.id, 1)}>+</button>
                </div>
                <button
                  className="remove-button"
                  onClick={() => removeFromCart(item.id)}
                >
                  Supprimer
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {cart.length > 0 && (
        <button
          className="validate-cart-button"
          onClick={() => navigate("/checkout")}
        >
          Valider mon panier
        </button>
      )}
    </div>
  );
};

export default Cart;
