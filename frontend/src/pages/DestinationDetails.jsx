
import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { getDestinationById } from '../services/destinationService'
import './DestinationDetails.css'

function DestinationDetails() {
  const { id } = useParams()

  const [destination, setDestination] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [retryCount, setRetryCount] = useState(0)

  useEffect(() => {
    let isActive = true

    const fetchDestination = async () => {
      setLoading(true)
      setError('')
      setDestination(null)

      try {
        const response = await getDestinationById(id)

        if (isActive) {
          setDestination(response.data)
        }
      } catch (error) {
        console.error('Error fetching destination:', error)

        if (isActive) {
          setError('Unable to load this destination. Please try again.')
        }
      } finally {
        if (isActive) {
          setLoading(false)
        }
      }
    }

    fetchDestination()

    return () => {
      isActive = false
    }
  }, [id, retryCount])

  if (loading) {
    return (
      <main className="destination-status">
        <p>Loading destination...</p>
      </main>
    )
  }

  if (error) {
    return (
      <main className="destination-status">
        <h2>Something went wrong</h2>
        <p>{error}</p>

        <button
          className="details-retry-button"
          onClick={() => setRetryCount((count) => count + 1)}
        >
          Try Again
        </button>

        <Link to="/#destinations" className="back-link">
          ← Back to destinations
        </Link>
      </main>
    )
  }

  if (!destination) {
    return (
      <main className="destination-status">
        <h2>Destination not found</h2>
        <p>We couldn't find the destination you're looking for.</p>

        <Link to="/#destinations" className="back-link">
          ← Explore other destinations
        </Link>
      </main>
    )
  }

  const imageUrl = destination.image
    ? `http://127.0.0.1:8000${destination.image}`
    : 'https://placehold.co/1200x700?text=Destination'

  return (
    <main className="destination-details">
      <div className="details-navigation">
        <Link to="/#destinations" className="back-link">
          ← Back to destinations
        </Link>

        <Link to="/" className="details-brand">
          Unknown Roads<span>.</span>
        </Link>
      </div>

      <section className="details-hero">
        <img
          src={imageUrl}
          alt={destination.name}
          className="details-hero-image"
        />

        <div className="details-hero-overlay">
          <p className="details-eyebrow">
            DISCOVER YOUR NEXT JOURNEY
          </p>

          <h1>{destination.name}</h1>

          <p className="details-hero-location">
            <span aria-hidden="true">⌖</span>{' '}
            {destination.location}, {destination.state}
          </p>
        </div>
      </section>

      <section className="details-content">
        <div className="details-main">
          <p className="details-section-label">
            ABOUT THIS DESTINATION
          </p>

          <h2>Discover {destination.name}</h2>

          <p className="details-description">
            {destination.description}
          </p>

          {destination.categories?.length > 0 && (
            <div className="details-categories-section">
              <h3>What kind of trip is this?</h3>

              <div className="details-categories">
                {destination.categories.map((category) => (
                  <span
                    className="details-category-tag"
                    key={category.id}
                  >
                    {category.name}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        <aside className="details-sidebar">
          <p className="details-section-label">
            YOUR NEXT ADVENTURE
          </p>

          <h3>Ready to explore?</h3>

          <p>
            Discover more places and find the journey that's right for you.
          </p>

          <Link
            to="/#destinations"
            className="details-explore-button"
          >
            Explore more destinations
          </Link>
        </aside>
      </section>
    </main>
  )
}

export default DestinationDetails
