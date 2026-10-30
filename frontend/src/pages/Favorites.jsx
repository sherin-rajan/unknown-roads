import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import {
  getFavorites,
  removeFavorite,
} from '../services/favoriteService'

function Favorites() {
  const [favorites, setFavorites] = useState([])
  const [loading, setLoading] = useState(true)
  const [removingId, setRemovingId] = useState(null)
  const [error, setError] = useState('')

  const loadFavorites = async () => {
    try {
      setError('')
      const data = await getFavorites()
      setFavorites(data)
    } catch (err) {
      console.error('Failed to load favorites:', err)
      setError('Unable to load your saved destinations. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadFavorites()
  }, [])

  const handleRemove = async (favoriteId) => {
    setRemovingId(favoriteId)
    setError('')

    try {
      await removeFavorite(favoriteId)

      setFavorites((previous) =>
        previous.filter((favorite) => favorite.id !== favoriteId)
      )
    } catch (err) {
      console.error('Failed to remove favorite:', err)
      setError('Unable to remove this destination. Please try again.')
    } finally {
      setRemovingId(null)
    }
  }

  const getImageUrl = (image) => {
    if (!image) return null

    return image.startsWith('http')
      ? image
      : `http://127.0.0.1:8000${image}`
  }

  return (
    <div className="app">
      <Navbar />

      <main className="favorites-page">
        <section className="favorites-heading">
          <p className="section-label">YOUR TRAVEL COLLECTION</p>
          <h1>Places You Love</h1>
          <p>
            Keep your favourite destinations close and find inspiration
            for your next adventure.
          </p>
        </section>

        {error && (
          <div className="form-error">
            {error}
            {!loading && (
              <button type="button" onClick={loadFavorites}>
                Try Again
              </button>
            )}
          </div>
        )}

        {loading ? (
          <p className="empty-message">Loading your saved destinations...</p>
        ) : favorites.length === 0 ? (
          <section className="favorites-empty">
            <div className="favorites-empty-icon">🌿</div>
            <h2>Your journey starts here</h2>
            <p>
              You haven't saved any destinations yet. Explore beautiful
              places and save the ones you'd love to visit.
            </p>
            <Link to="/#destinations" className="favorites-explore-button">
              Explore Destinations
            </Link>
          </section>
        ) : (
          <>
            <div className="favorites-count">
              <p>
                You have saved <strong>{favorites.length}</strong>{' '}
                {favorites.length === 1 ? 'destination' : 'destinations'}.
              </p>
            </div>

            <section className="favorites-grid">
              {favorites.map((favorite) => (
                <article className="favorite-card" key={favorite.id}>
                  <div className="favorite-image">
                    {favorite.destination_image ? (
                      <img
                        src={getImageUrl(favorite.destination_image)}
                        alt={favorite.destination_name}
                      />
                    ) : (
                      <div className="favorite-image-placeholder">
                        🌿
                      </div>
                    )}
                  </div>

                  <div className="favorite-card-content">
                    <p className="favorite-location">
                      {favorite.destination_state}
                      {favorite.destination_location
                        ? ` · ${favorite.destination_location}`
                        : ''}
                    </p>

                    <h2>{favorite.destination_name}</h2>

                    <div className="favorite-card-actions">
                      <Link
                        to={`/destinations/${favorite.destination}`}
                      >
                        Explore Place
                      </Link>

                      <button
                        type="button"
                        onClick={() => handleRemove(favorite.id)}
                        disabled={removingId === favorite.id}
                      >
                        {removingId === favorite.id
                          ? 'Removing...'
                          : 'Remove'}
                      </button>
                    </div>
                  </div>
                </article>
              ))}
            </section>
          </>
        )}
      </main>
    </div>
  )
}

export default Favorites
