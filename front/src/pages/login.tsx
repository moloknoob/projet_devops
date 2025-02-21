import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";

const Login = () => {
  const [formData, setFormData] = useState({ email: "", password: "" });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("");

    try {
      const response = await fetch("http://localhost:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("Connexion réussie !");
        localStorage.setItem("token", data.token);
        setTimeout(() => navigate("/product"), 2000);
      } else {
        setMessage(data.message || "Email ou mot de passe incorrect.");
      }
    } catch (error) {
      setMessage("Erreur de connexion au serveur.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        <h1>Connexion</h1>

        {message && (
          <p
            className={`message ${
              message.includes("réussie") ? "success" : "error"
            }`}
          >
            {message}
          </p>
        )}

        <form onSubmit={handleSubmit} className="login-form">
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="Email"
            className="input-field"
            autoFocus
            required
          />
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            placeholder="Mot de passe"
            className="input-field"
            required
          />
          <button type="submit" className="submit-btn">
            Se connecter
          </button>
        </form>

        <p className="register-link">
          Pas encore de compte ? <a href="/register">Inscrivez-vous</a>
        </p>
      </div>
    </div>
  );
};

export default Login;
