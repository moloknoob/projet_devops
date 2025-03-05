import { useNavigate } from "react-router-dom";

const About = () => {
  const navigate = useNavigate();

  return (
    <div className="about-container">
      <h1>À Propos de Nous</h1>
      <p>
        Bienvenue sur <strong>AnimeShop</strong>, la boutique en ligne dédiée
        aux passionnés d'anime ! 🎌✨
      </p>
      <p>
        Nous proposons une large sélection de figurines, posters, vêtements et
        objets de collection inspirés de vos séries animées préférées. Que vous
        soyez fan de <em>One Piece</em>, <em>Naruto</em>,<em>Dragon Ball</em> ou
        d'autres classiques, vous trouverez votre bonheur chez nous !
      </p>
      <p>
        Notre mission est d'apporter aux fans d'anime des produits de qualité,
        soigneusement sélectionnés et livrés avec passion. 🛒💖
      </p>
      <p>
        Rejoignez la communauté et collectionnez vos héros préférés dès
        maintenant ! 🚀
      </p>

      <div className="about-buttons">
        <button onClick={() => navigate("/register")}>Inscription</button>
        <button onClick={() => navigate("/login")}>Connexion</button>
        <button onClick={() => navigate("/products")}>Nos Produits</button>
      </div>
    </div>
  );
};

export default About;
