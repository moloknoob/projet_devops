import React from "react";
import "../styles/product.css";

const Product = () => {
  return (
    <div className="product-container">
      <h2 className="product-title">Nos Produits</h2>
      <div className="product-list">
        <div className="product-card">
          <img
            src="/images/escanor.jpg"
            alt="Produit 1"
            className="product-image"
          />
          <button className="buy-button">Acheter</button>
        </div>
        <div className="product-card">
          <img
            src="/images/Guts.webp"
            alt="Produit 2"
            className="product-image"
          />
          <button className="buy-button">Acheter</button>
        </div>
        <div className="product-card">
          <img
            src="/images/Ken.jpg"
            alt="Produit 3"
            className="product-image"
          />
          <button className="buy-button">Acheter</button>
        </div>
      </div>
    </div>
  );
};

export default Product;
