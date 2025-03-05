// src/App.tsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./pages/register"; // Import de la page Register
import Login from "./pages/login";
import Product from "./pages/product";
import Order from "./pages/order";
import Cart from "./pages/card";
import Home from "./pages/home";
import About from "./pages/about";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/product" element={<Product />} />
        <Route path="/order" element={<Order />} />
        <Route path="/card" element={<Cart />} />
        <Route path="/card" element={<Cart />} />
      </Routes>
    </Router>
  );
}

export default App;
