
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function Navbar() {
  const { user, loading, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = async () => {
    try {
      await logout()
      navigate('/', { replace: true })
    } catch (error) {
      console.error('Logout failed:', error)
    }
  }

  return (
    <nav className="navbar">
      <Link to="/" className="logo">
        Unknown Roads<span>.</span>
      </Link>

      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/#destinations">Destinations</Link>

        {!loading && (
          user ? (
            <>
              <Link to="/dashboard">Dashboard</Link>
              <Link to="/favorites">Saved Destinations</Link>

              <button
                type="button"
                className="nav-button"
                onClick={handleLogout}
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="nav-button">
                Login
              </Link>

              <Link to="/register" className="nav-button">
                Register
              </Link>
            </>
          )
        )}
      </div>
    </nav>
  )
}

export default Navbar
