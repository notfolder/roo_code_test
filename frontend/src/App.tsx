import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import LoginPage from './pages/LoginPage'
import PrivateRoute from './components/PrivateRoute'
import EquipmentListPage from './pages/EquipmentListPage'
import EquipmentManagePage from './pages/EquipmentManagePage'
import LoanManagePage from './pages/LoanManagePage'
import LoanHistoryPage from './pages/LoanHistoryPage'

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />

        {/* 認証済みユーザー共通ルート */}
        <Route element={<PrivateRoute />}>
          <Route path="/" element={<EquipmentListPage />} />
          <Route path="/loans/history" element={<LoanHistoryPage />} />
        </Route>

        {/* ADMIN 専用ルート */}
        <Route element={<PrivateRoute requiredRole="ADMIN" />}>
          <Route path="/equipments/manage" element={<EquipmentManagePage />} />
          <Route path="/loans" element={<LoanManagePage />} />
        </Route>

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  )
}

export default App
