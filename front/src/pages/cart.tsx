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
        if (!token)
          throw new Error("Veuillez vous connecter pour voir votre panier.");

        // Décodage du token pour récupérer l'ID utilisateur
        const decodedToken = JSON.parse(atob(token.split(".")[1]));
        const userId = decodedToken.sub;

        const response = await fetch(`http://localhost:5000/cart/${userId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (!response.ok)
          throw new Error("Erreur lors du chargement du panier.");

        const data = await response.json();
        setCart(
          data.map((item: CartItem) => ({
            ...item,
            total_price: item.product_price * item.quantity,
          }))
        );
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchCart();
  }, [token]);

  // Supprimer un produit du panier
  const removeFromCart = async (itemId: number) => {
    try {
      const response = await fetch(`http://localhost:5000/cart/${itemId}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok)
        throw new Error("Erreur lors de la suppression du produit.");
      setCart(cart.filter((item) => item.id !== itemId));
    } catch (err: any) {
      setError(err.message);
    }
  };

  // Modifier la quantité d'un produit
  const updateQuantity = async (itemId: number, newQuantity: number) => {
    if (newQuantity < 1) return;
    try {
      const response = await fetch(`http://localhost:5000/cart/${itemId}`, {
        method: "PUT",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ quantity: newQuantity }),
      });
      if (!response.ok)
        throw new Error("Erreur lors de la mise à jour de la quantité.");
      setCart(
        cart.map((item) =>
          item.id === itemId
            ? {
                ...item,
                quantity: newQuantity,
                total_price: newQuantity * item.product_price,
              }
            : item
        )
      );
    } catch (err: any) {
      setError(err.message);
    }
  };

  // Calcul du total général sécurisé
  const totalGeneral = cart
    .reduce((acc, item) => acc + (item.total_price || 0), 0)
    .toFixed(2);

  // Gestion des erreurs et du chargement
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
                src={`http://localhost:5000/${item.image}`}
                alt={item.product_name}
                className="cart-item-image"
              />
              <div className="cart-item-details">
                <h3>{item.product_name}</h3>
                <p>{item.product_description}</p>
                <p>
                  Prix : {item.product_price} € x {item.quantity}
                </p>
                <p>Total : {item.total_price.toFixed(2)} €</p>
                <div className="cart-item-actions">
                  <button
                    onClick={() => updateQuantity(item.id, item.quantity - 1)}
                  >
                    -
                  </button>
                  <span>{item.quantity}</span>
                  <button
                    onClick={() => updateQuantity(item.id, item.quantity + 1)}
                  >
                    +
                  </button>
                  <button onClick={() => removeFromCart(item.id)}>
                    🗑 Supprimer
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
      {cart.length > 0 && (
        <div className="cart-actions">
          <p>
            <strong>Total général : {totalGeneral} €</strong>
          </p>
          <button
            className="continue-shopping"
            onClick={() => navigate("/product")}
          >
            Continuer vos achats
          </button>
          <button
            className="validate-cart-button"
            onClick={() => navigate("/payment")}
          >
            Valider la commande & payer
          </button>
        </div>
      )}
    </div>
  );
};

export default Cart;
