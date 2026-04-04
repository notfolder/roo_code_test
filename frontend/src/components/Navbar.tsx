import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <nav style={{ background: '#1976d2', color: '#fff', padding: '0 1.5rem', display: 'flex', alignItems: 'center', height: '56px', gap: '1.5rem' }}>
      <span style={{ fontWeight: 700, fontSize: '1.1rem', marginRight: '1rem' }}>備品管理システム</span>

      <Link to="/" style={linkStyle}>備品一覧</Link>
      <Link to="/loans/history" style={linkStyle}>自分の貸出履歴</Link>

      {user?.role === 'ADMIN' && (
        <>
          <Link to="/equipments/manage" style={linkStyle}>備品管理</Link>
          <Link to="/loans" style={linkStyle}>貸出・返却管理</Link>
        </>
      )}

      <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '1rem' }}>
        {user && <span style={{ fontSize: '0.875rem' }}>{user.name}</span>}
        <button onClick={handleLogout} style={logoutButtonStyle}>ログアウト</button>
      </div>
    </nav>
  )
}

const linkStyle: React.CSSProperties = {
  color: '#fff',
  textDecoration: 'none',
  fontSize: '0.95rem',
  padding: '0.25rem 0.5rem',
  borderRadius: '4px',
}

const logoutButtonStyle: React.CSSProperties = {
  background: 'rgba(255,255,255,0.2)',
  color: '#fff',
  border: '1px solid rgba(255,255,255,0.5)',
  borderRadius: '4px',
  padding: '0.25rem 0.75rem',
  cursor: 'pointer',
  fontSize: '0.875rem',
}
