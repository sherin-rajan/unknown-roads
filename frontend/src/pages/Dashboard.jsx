import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Navbar from '../components/Navbar'
import { getFavorites } from '../services/favoriteService'

function Dashboard() {
  const { user } = useAuth()

  const [favoriteCount, setFavoriteCount] = useState(0)
  const [loadingFavorites, setLoadingFavorites] = useState(true)

  useEffect(() => {
    const loadFavoriteCount = async () => {
      try {
        const favorites = await getFavorites()
        setFavoriteCount(favorites.length)
      } catch (error) {
        console.error('Failed to load favorite count:', error)
      } finally {
        setLoadingFavorites(false)
      }
    }

    loadFavoriteCount()
  }, [])

  return (
    <div className="app">
      <Navbar />

      <main className="dashboard">

        {/* Welcome Section */}
        <section className="dashboard-welcome">
          <p className="section-label">YOUR TRAVEL SPACE</p>

          <h1>
            Welcome back, {user?.first_name || user?.username}!
          </h1>

          <p>
            Your next adventure is waiting. Manage your account,
            revisit saved places, and discover somewhere new.
          </p>
        </section>

        {/* Travel Overview */}
        <section className="dashboard-overview">
          <div className="dashboard-overview-card">
            <span className="dashboard-icon">❤️</span>
            <div>
              <h2>
                {loadingFavorites ? '...' : favoriteCount}
              </h2>
              <p>Saved Destinations</p>
            </div>
          </div>

          <div className="dashboard-overview-card">
            <span className="dashboard-icon">👤</span>
            <div>
              <h2>Customer</h2>
              <p>Account Type</p>
            </div>
          </div>
        </section>

        {/* Account Actions */}
        <section className="dashboard-section">
          <div className="dashboard-section-heading">
            <p className="section-label">YOUR ACCOUNT</p>
            <h2>Manage Your Account</h2>
          </div>

          <div className="dashboard-grid">

            <Link to="/profile" className="dashboard-card">
              <span className="dashboard-icon">👤</span>
              <h2>My Profile</h2>
              <p>
                View and update your personal information.
              </p>
            </Link>

            <Link to="/favorites" className="dashboard-card">
              <span className="dashboard-icon">❤️</span>
              <h2>Saved Destinations</h2>
              <p>
                Revisit the places you have added to your collection.
              </p>
            </Link>

            <Link to="/change-password" className="dashboard-card">
              <span className="dashboard-icon">🔒</span>
              <h2>Change Password</h2>
              <p>
                Keep your account secure by updating your password.
              </p>
            </Link>

          </div>
        </section>

        {/* Discover Section */}
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
