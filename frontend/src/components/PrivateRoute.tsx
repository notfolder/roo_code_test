import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import Navbar from './Navbar'

interface PrivateRouteProps {
  requiredRole?: 'ADMIN' | 'USER'
}

export default function PrivateRoute({ requiredRole }: PrivateRouteProps) {
  const { token, user } = useAuth()

  if (!token || !user) {
    return <Navigate to="/login" replace />
  }

  if (requiredRole === 'ADMIN' && user.role !== 'ADMIN') {
    return <Navigate to="/" replace />
  }

  return (
    <>
      <Navbar />
      <main style={{ padding: '1.5rem' }}>
        <Outlet />
      </main>
    </>
  )
}
