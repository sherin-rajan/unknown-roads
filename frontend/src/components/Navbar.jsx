import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="logo">
        Unknown Roads<span>.</span>
      </Link>

      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/">Destinations</Link>
        <Link to="/login" className="nav-button">
          Login
        </Link>
        <Link to="/register" className="nav-button">
          Register
        </Link>
      </div>
    </nav>
  )
}

export default Navbar