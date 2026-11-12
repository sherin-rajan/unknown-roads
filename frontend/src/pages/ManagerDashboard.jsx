import { useEffect, useState } from 'react'

import Navbar from '../components/Navbar'
import { getManagerDashboard } from '../services/dashboardService'

function ManagerDashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadDashboard = async () => {
    setLoading(true)
    setError('')

    try {
      const data = await getManagerDashboard()
      setStats(data)
    } catch (err) {
      console.error('Manager dashboard loading failed:', err)
      setError('Unable to load the manager dashboard. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadDashboard()
  }, [])

  const dashboardCards = [
    {
      icon: '🧭',
      label: 'Total Packages',
      value: stats?.total_packages,
    },
    {
      icon: '🌿',
      label: 'Published Packages',
      value: stats?.published_packages,
    },
    {
      icon: '🧳',
      label: 'Total Bookings',
      value: stats?.total_bookings,
    },
    {
      icon: '⏳',
      label: 'Pending Bookings',
      value: stats?.pending_bookings,
    },
    {
      icon: '✉️',
      label: 'New Enquiries',
      value: stats?.new_enquiries,
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

      <main className="dashboard manager-dashboard">
        <section className="dashboard-welcome">
          <p className="section-label">UNKNOWN ROADS MANAGEMENT</p>

          <h1>Manager Dashboard</h1>

          <p>
            Welcome! Monitor your travel packages, bookings,
            customer enquiries, and notifications.
          </p>
        </section>

        <section className="dashboard-section">
          <div className="dashboard-section-heading">
            <p className="section-label">BUSINESS OVERVIEW</p>
            <h2>Company Summary</h2>
          </div>

          {loading && (
            <p className="empty-message">
              Loading management summary...
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
            <div className="dashboard-overview manager-overview">
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
      </main>
    </div>
  )
}

export default ManagerDashboard