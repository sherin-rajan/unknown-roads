import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

import { useAuth } from '../context/AuthContext'
import Navbar from '../components/Navbar'
import { getCustomerDashboard } from '../services/dashboardService'

function Dashboard() {
  const { user } = useAuth()

  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadDashboard = async () => {
    setLoading(true)
    setError('')

    try {
      const data = await getCustomerDashboard()
      setStats(data)
    } catch (err) {
      console.error('Customer dashboard loading failed:', err)
      setError('Unable to load your dashboard. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadDashboard()
  }, [])

  const dashboardCards = [
    {
      icon: '🧳',
      label: 'Total Bookings',
      value: stats?.total_bookings,
    },
    {
      icon: '🗺️',
      label: 'Upcoming Trips',
      value: stats?.upcoming_trips,
    },
    {
      icon: '⏳',
      label: 'Pending Bookings',
      value: stats?.pending_bookings,
    },
    {
      icon: '✉️',
      label: 'My Enquiries',
      value: stats?.total_enquiries,
    },
    {
      icon: '🔔',
      label: 'Unread Notifications',
      value: stats?.unread_notifications,
    },
  ]

  return (
    <div className="app">
      <Navbar />

      <main className="dashboard">
        <section className="dashboard-welcome">
          <p className="section-label">YOUR TRAVEL SPACE</p>

          <h1>
            Welcome back, {user?.first_name || user?.username}!
          </h1>

          <p>
            Keep track of your bookings, upcoming journeys,
            and travel enquiries in one place.
          </p>
        </section>

        <section className="dashboard-section">
          <div className="dashboard-section-heading">
            <p className="section-label">YOUR OVERVIEW</p>
            <h2>Your Travel Summary</h2>
          </div>

          {loading && (
            <p className="empty-message">
              Loading your travel summary...
            </p>
          )}

          {error && (
            <div className="error-message">
              {error}
              <br />
              <button
                type="button"
                className="dashboard-retry-button"
                onClick={loadDashboard}
              >
                Try Again
              </button>
            </div>
          )}

          {!loading && !error && stats && (
            <div className="dashboard-overview">
              {dashboardCards.map((card) => (
                <div className="dashboard-overview-card" key={card.label}>
                  <span className="dashboard-icon">{card.icon}</span>

                  <div>
                    <h2>{card.value}</h2>
                    <p>{card.label}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="dashboard-section">
          <div className="dashboard-section-heading">
            <p className="section-label">YOUR ACCOUNT</p>
            <h2>Manage Your Account</h2>
          </div>

          <div className="dashboard-grid">
            <Link to="/profile" className="dashboard-card">
              <span className="dashboard-icon">👤</span>
              <h2>My Profile</h2>
              <p>View and update your personal information.</p>
            </Link>

            <Link to="/favorites" className="dashboard-card">
              <span className="dashboard-icon">❤️</span>
              <h2>Saved Destinations</h2>
              <p>Revisit the places you have saved.</p>
            </Link>

            <Link to="/change-password" className="dashboard-card">
              <span className="dashboard-icon">🔒</span>
              <h2>Change Password</h2>
              <p>Keep your account secure.</p>
            </Link>
          </div>
        </section>

        <section className="dashboard-discover">
          <div>
            <p className="section-label">FIND YOUR NEXT ADVENTURE</p>
            <h2>There is always somewhere new to explore.</h2>
            <p>
              Discover beautiful landscapes, unique cultures,
              and unforgettable festivals.
            </p>
          </div>

          <Link to="/#destinations" className="dashboard-explore-button">
            Explore Destinations
          </Link>
        </section>
      </main>
    </div>
  )
}

export default Dashboard