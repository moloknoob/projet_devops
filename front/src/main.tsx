import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { BrowserRouter } from "react-router-dom";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BrowserRouter>
      {" "}
      {/* Enveloppe App avec BrowserRouter  permet de gerer les routes */}
      <App />
    </BrowserRouter>
  </StrictMode>
);
