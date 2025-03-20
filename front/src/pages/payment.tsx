import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

interface CartItem {
  id: number;
  product_id: number;
  product_name: string;
  quantity: number;
  total_price: number;
  image: string;
}

interface Payment {
  order_id: number;
  payment_method: string;
  payment_status: string;
}

interface OrderPaymentProps {
  userId: number;
}

const OrderPayment: React.FC<OrderPaymentProps> = ({ userId }) => {
  console.log("👤 User ID reçu dans OrderPayment:", userId);

  const [cart, setCart] = useState<CartItem[]>([]);
  const [orderId, setOrderId] = useState<number | null>(null);
  const [paymentMethod, setPaymentMethod] = useState<string>("carte");
  const [payments, setPayments] = useState<Payment[]>([]);
  const [message, setMessage] = useState<string>("");

  const navigate = useNavigate();

  // Récupérer le panier
  useEffect(() => {
    console.log(`🔄 Chargement du panier pour userId: ${userId}...`);

    fetch(`http://localhost:5000/cart/${userId}`)
      .then((res) => {
        console.log("✅ Réponse API panier reçue :", res);
        return res.json();
      })
      .then((data) => {
        console.log("📦 Données panier récupérées :", data);
        setCart(data);
      })
      .catch((err) => console.error("❌ Erreur chargement panier :", err));
  }, [userId]);

  // Créer une commande
  const handleCreateOrder = () => {
    console.log("📝 Création de commande en cours...");

    fetch("http://localhost:5000/create-order", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId }),
    })
      .then((res) => res.json())
      .then((data: { order_id?: number; message?: string }) => {
        if (data.order_id) {
          console.log("✅ Commande créée avec ID:", data.order_id);
          setOrderId(data.order_id);
          setMessage("Commande créée avec succès !");
        } else {
          console.log(
            "❌ Erreur lors de la création de la commande:",
            data.message
          );
          setMessage(
            data.message || "Erreur lors de la création de la commande."
          );
        }
      })
      .catch((err) => console.error("❌ Erreur lors de la commande :", err));
  };

  // Effectuer un paiement
  const handlePayment = () => {
    if (!orderId) {
      console.warn("⚠️ Aucune commande trouvée pour effectuer un paiement !");
      return;
    }

    console.log(
      `💳 Paiement en cours pour la commande ${orderId} avec méthode ${paymentMethod}...`
    );

    fetch("http://localhost:5000/pay-order", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        order_id: orderId,
        payment_method: paymentMethod,
      }),
    })
      .then((res) => res.json())
      .then((data: { message: string }) => {
        console.log("✅ Réponse API paiement :", data.message);
        setMessage(data.message);

        if (data.message === "Paiement effectué avec succès") {
          setCart([]);
          setOrderId(null);
        }
      })
      .catch((err) => console.error("❌ Erreur paiement :", err));
  };

  // Charger l'historique des paiements
  useEffect(() => {
    console.log(`🔄 Chargement des paiements pour userId: ${userId}...`);

    fetch(`http://localhost:5000/payments/${userId}`)
      .then((res) => res.json())
      .then((data: Payment[]) => {
        console.log("📜 Historique des paiements :", data);
        setPayments(data);
      })
      .catch((err) => console.error("❌ Erreur chargement paiements :", err));
  }, [userId]);

  return (
    <div className="order-payment-container">
      <h2>🛒 Mon Panier</h2>
      {cart.length > 0 ? (
        cart.map((item) => (
          <div key={item.id}>
            <img
              src={`http://localhost:5000/${item.image}`}
              alt={item.product_name}
              style={{ width: "50px", height: "50px", objectFit: "cover" }}
            />
            {item.product_name} x{item.quantity} - {item.total_price}€
          </div>
        ))
      ) : (
        <p>Votre panier est vide.</p>
      )}

      <button onClick={handleCreateOrder} disabled={cart.length === 0}>
        Créer ma commande
      </button>

      {orderId && (
        <div>
          <h3>💳 Paiement</h3>
          <select onChange={(e) => setPaymentMethod(e.target.value)}>
            <option value="carte">Carte bancaire</option>
            <option value="paypal">PayPal</option>
            <option value="virement">Virement bancaire</option>
          </select>
          <button onClick={handlePayment}>Payer</button>
        </div>
      )}

      <h2>📜 Historique des paiements</h2>
      {payments.length > 0 ? (
        payments.map((payment) => (
          <div key={payment.order_id}>
            Commande {payment.order_id} - {payment.payment_method} -{" "}
            {payment.payment_status}
          </div>
        ))
      ) : (
        <p>Aucun paiement trouvé.</p>
      )}

      {message && <p>{message}</p>}
    </div>
  );
};

export default OrderPayment;
