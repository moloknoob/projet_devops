import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./pages/register";
import Login from "./pages/login";
import Product from "./pages/product";
import Order from "./pages/order";
import Cart from "./pages/cart";
import Home from "./pages/home";
import About from "./pages/about";
import OrderPayment from "./pages/payment";

// Fonction pour récupérer l'ID utilisateur depuis le token JWT
const getUserIdFromToken = (): number | null => {
  const token = localStorage.getItem("token");
  if (!token) return null;

  try {
    const payload = JSON.parse(atob(token.split(".")[1])); // Décoder le payload JWT
    return payload.sub; // Supposons que 'sub' contient l'ID utilisateur
  } catch (error) {
    console.error("Erreur de décodage du token :", error);
    return null;
  }
};

function App() {
  const userId = getUserIdFromToken(); // Récupérer l'ID utilisateur

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/product" element={<Product />} />
        <Route path="/order" element={<Order />} />
        <Route path="/cart" element={<Cart />} />

        {/* Vérifier si userId est présent avant d'afficher la page de paiement */}
        {userId ? (
          <Route path="/payment" element={<OrderPayment userId={userId} />} />
        ) : (
          <Route path="/payment" element={<Login />} /> // Rediriger vers login si non connecté
        )}
      </Routes>
    </Router>
  );
}

export default App;
