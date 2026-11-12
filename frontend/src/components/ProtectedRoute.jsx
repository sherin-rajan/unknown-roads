import { Navigate, Outlet, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function ProtectedRoute({ allowedRoles }) {
  const { user, loading } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div className="empty-message">
        Checking your account...
      </div>
    )
  }

  if (!user) {
    return (
      <Navigate
        to="/login"
        state={{ from: location.pathname }}
        replace
      />
    )
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    const correctDashboard =
      user.role === 'manager'
        ? '/manager-dashboard'
        : '/dashboard'

    return <Navigate to={correctDashboard} replace />
  }

  return <Outlet />
}

export default ProtectedRoute