import { Routes, Route, Navigate } from "react-router-dom";
import { Layout } from "./components/Layout";
import { EquipmentListPage } from "./pages/EquipmentListPage";
import { ReservationPage } from "./pages/ReservationPage";
import { AvailabilityPage } from "./pages/AvailabilityPage";
import { LoginPage } from "./pages/LoginPage";

// ルーティング定義
export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/equipment" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/equipment" element={<EquipmentListPage />} />
        <Route path="/availability" element={<AvailabilityPage />} />
        <Route path="/reservations" element={<ReservationPage />} />
        <Route path="*" element={<Navigate to="/equipment" replace />} />
      </Routes>
    </Layout>
  );
}
