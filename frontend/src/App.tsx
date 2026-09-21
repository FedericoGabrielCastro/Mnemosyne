import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { Gate } from "./pages/Gate";
import { Palace } from "./pages/Palace";
import { Vaults } from "./pages/Vaults";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Gate />} />
        <Route path="/vaults" element={<Vaults />} />
        <Route path="/vaults/:vaultId" element={<Palace />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
