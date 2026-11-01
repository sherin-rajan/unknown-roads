
import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function Login() {
  const navigate = useNavigate()
  const location = useLocation()
  const { login } = useAuth()

  const [credentials, setCredentials] = useState({
    username: '',
    password: '',
  })

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleChange = (event) => {
    setCredentials({
      ...credentials,
      [event.target.name]: event.target.value,
    })
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')
    setLoading(true)

    try {
      const currentUser = await login(credentials)

      // Redirect users according to their role
      let dashboardPath = '/dashboard'

      if (currentUser.role === 'admin') {
        dashboardPath = '/admin-dashboard'
      } else if (currentUser.role === 'manager') {
        dashboardPath = '/manager-dashboard'
      }

      // Respect the originally requested page for customers
      const destination =
        currentUser.role === 'customer'
          ? (location.state?.from || dashboardPath)
          : dashboardPath

      navigate(destination, { replace: true })

    } catch (err) {
      const data = err.response?.data

      setError(
        data?.detail ||
        data?.error ||
        'Login failed. Check your username and password.'
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <Link to="/" className="auth-brand">Unknown Roads</Link>
        <h1>Welcome back</h1>
        <p>Log in to continue your travel journey.</p>

        {location.state?.message && (
          <div className="auth-success" role="status">
            {location.state.message}
          </div>
        )}

        {error && <div className="auth-error" role="alert">{error}</div>}

        <form onSubmit={handleSubmit}>
          <label htmlFor="username">Username</label>
          <input
            id="username"
            name="username"
            value={credentials.username}
            onChange={handleChange}
            autoComplete="username"
            required
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            name="password"
            type="password"
            value={credentials.password}
            onChange={handleChange}
            autoComplete="current-password"
            required
          />

          <button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Log in'}
          </button>
        </form>

        <p className="auth-footer">
          Don't have an account? <Link to="/register">Create one</Link>
        </p>
      </section>
    </main>
  )
}

export default Login
