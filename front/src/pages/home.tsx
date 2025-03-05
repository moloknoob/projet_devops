import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1>Bienvenue sur mon site ! 🎉</h1>
      <p>Découvrez nos produits et profitez des meilleures offres.</p>

      <div className="buttons">
        <button onClick={() => navigate("/login")}>Connexion</button>
        <button onClick={() => navigate("/register")}>Inscription</button>
        <button onClick={() => navigate("/about")}>À Propos</button>
      </div>
    </div>
  );
};

export default Home;
