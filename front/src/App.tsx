// src/App.tsx
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./pages/register"; // Import de la page Register
import Login from "./pages/login";
import Product from "./pages/product";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
        <Route path="/product" element={<Product />} />
      </Routes>
    </Router>
  );
}

export default App;
