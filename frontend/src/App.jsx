import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [destinations, setDestinations] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState('')
  const [searchTerm, setSearchTerm] = useState('')

  
useEffect(() => {
  setLoading(true)

  const params = new URLSearchParams()

  if (selectedCategory) {
    params.append('category', selectedCategory)
  }

  if (searchTerm.trim()) {
    params.append('search', searchTerm.trim())
  }

  const query = params.toString()
  const url = query
    ? `http://127.0.0.1:8000/api/destinations/?${query}`
    : 'http://127.0.0.1:8000/api/destinations/'

  fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error('Failed to fetch destinations')
      }
      return response.json()
    })
    .then((data) => {
      setDestinations(data.results)
    })
    .catch((error) => {
      console.error('Error fetching destinations:', error)
      setDestinations([])
    })
    .finally(() => {
      setLoading(false)
    })
}, [selectedCategory, searchTerm])



  return (
    <div className="app">
      <nav className="navbar">
        <h1 className="logo">Via Maris<span>.</span></h1>

        <div className="nav-links">
          <a href="/">Home</a>
          <a href="#destinations">Destinations</a>
          <a href="#about">About</a>
        </div>

        <button className="nav-button">Explore Trips</button>
      </nav>

      <main>
        <section className="hero">
          <p className="hero-tagline">YOUR NEXT ADVENTURE STARTS HERE</p>

          <h2>
            Discover places.
            <br />
            Create memories.
          </h2>

          <p className="hero-description">
            Explore beautiful destinations, discover hidden gems,
            and find the journey that's right for you.
          </p>

          <a href="#destinations" className="hero-button">
            Explore Destinations →
          </a>
        </section>


        <section className="intro" id="destinations">
          <p className="section-label">EXPLORE THE WORLD</p>
          <h2>Where will your next journey take you?</h2>
          <p>
            From peaceful escapes to adventurous trails,
            your next unforgettable experience awaits.
          </p>
        </section>

        <section className="destinations-section">
          <div className="destinations-heading">
            <div>
              <p className="section-label">HANDPICKED FOR YOU</p>
              <h2>Popular Destinations</h2>
            </div>
            <p>Find your next unforgettable escape.</p>
          </div>

          <div className="destination-search">
            <input
              type="text"
              placeholder="Search destinations by name, state, or location..."
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
            />
          </div>

          <div className="category-filters">
            <button
              className={selectedCategory === '' ? 'active' : ''}
              onClick={() => setSelectedCategory('')}
            >
              All Destinations
            </button>

            <button
              className={selectedCategory === 'Solo Trips' ? 'active' : ''}
              onClick={() => setSelectedCategory('Solo Trips')}
            >
              Solo Trips
            </button>

            <button
              className={selectedCategory === 'Family Trips' ? 'active' : ''}
              onClick={() => setSelectedCategory('Family Trips')}
            >
              Family Trips
            </button>

            <button
              className={selectedCategory === 'Honeymoon Trips' ? 'active' : ''}
              onClick={() => setSelectedCategory('Honeymoon Trips')}
            >
              Honeymoon Trips
            </button>

            <button
              className={selectedCategory === 'Adventurous Trips' ? 'active' : ''}
              onClick={() => setSelectedCategory('Adventurous Trips')}
            >
              Adventurous Trips
            </button>
          </div>

          <div className="destination-grid">
            {destinations.map((destination) => (
              <article className="destination-card" key={destination.id}>
                <img
                  src={
                    destination.image
                      ? `http://127.0.0.1:8000${destination.image}`
                      : 'https://placehold.co/600x400?text=Destination'
                  }
                  alt={destination.name}
                  className="destination-image"
                />

                <div className="destination-content">
                  <p className="destination-location">
                    {destination.location}, {destination.state}
                  </p>

                  <h3>{destination.name}</h3>

                  <p className="destination-description">
                    {destination.description}
                  </p>

                  <div className="destination-categories">
                    {destination.categories?.map((category) => (
                      <span key={category.id}>
                        {category.name}
                      </span>
                    ))}
                  </div>
                </div>
              </article>
            ))}
          </div>

          {loading ? (
            <p className="empty-message">Loading destinations...</p>
          ) : destinations.length === 0 ? (
            <p className="empty-message">No destinations found.</p>
          ) : null}
        </section>

      </main>
    </div>
  )
}

export default App
