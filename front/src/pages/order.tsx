import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/order.css";

interface OrderItem {
  product_id: number;
  quantity: number;
  price: number;
}

interface Order {
  id: number;
  total_price: number;
  status: string;
  created_at: string;
  items: OrderItem[];
}

const OrderPage = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  useEffect(() => {
    const fetchOrders = async () => {
      if (!token) {
        setError("Vous devez être connecté pour voir vos commandes.");
        setLoading(false);
        return;
      }

      try {
        const response = await fetch("http://localhost:5000/order", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          if (response.status === 401) {
            throw new Error(
              "Votre session a expiré. Veuillez vous reconnecter."
            );
          }
          throw new Error("Erreur lors de la récupération des commandes.");
        }

        const data = await response.json();
        setOrders(data.orders);
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [token]);

  if (loading) return <p>Chargement des commandes...</p>;
  if (error) return <p className="error-message">{error}</p>;

  return (
    <div className="order-container">
      <h2 className="order-title">Vos Commandes</h2>
      {orders.length === 0 ? (
        <p className="empty-message">Aucune commande trouvée.</p>
      ) : (
        <div className="order-list">
          {orders.map((order) => (
            <div key={order.id} className="order-card">
              <p className="order-id">Commande #{order.id}</p>
              <p className="order-status">Statut: {order.status}</p>
              <p className="order-price">Total: {order.total_price} €</p>
              <p className="order-date">Date: {order.created_at}</p>
              <div className="order-items">
                <h4>Produits :</h4>
                {order.items.map((item, index) => (
                  <p key={index}>
                    Produit #{item.product_id} - {item.quantity} x {item.price}{" "}
                    €
                  </p>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
      <button className="back-button" onClick={() => navigate(-1)}>
        Retour aux produits
      </button>
    </div>
  );
};

export default OrderPage;
