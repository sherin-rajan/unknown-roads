import { useEffect, useState } from 'react'
import { Routes, Route, Link} from 'react-router-dom'
import DestinationDetails from './pages/DestinationDetails'
import { getDestinations } from './services/destinationService'
import './App.css'

function App() {
  const [destinations, setDestinations] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedCategory, setSelectedCategory] = useState('')
  const [searchTerm, setSearchTerm] = useState('')
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState('')
  const [sortBy, setSortBy] = useState('featured')

  useEffect(() => {
  const timer = setTimeout(() => {
    setDebouncedSearchTerm(searchTerm)
  }, 400)

  return () => {
    clearTimeout(timer)
  }
  }, [searchTerm])

  useEffect(() => {
    const fetchDestinations = async () => {
      setLoading(true)

      try {
        const params = {}

        if (selectedCategory) {
          params.category = selectedCategory
        }

        if (debouncedSearchTerm.trim()) {
          params.search = debouncedSearchTerm.trim()
        }

        params.ordering = sortBy

        const response = await getDestinations(params)

        setDestinations(response.data.results)
      } catch (error) {
        console.error('Error fetching destinations:', error)
        setDestinations([])
      } finally {
        setLoading(false)
      }
    }

    fetchDestinations()
  }, [selectedCategory, debouncedSearchTerm, sortBy])

return (
  <Routes>
    <Route path="/" element={
      <div className="app">
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
          <div className="sort-control">
            <label htmlFor="sortBy">Sort by:</label>

            <select
              id="sortBy"
              value={sortBy}
              onChange={(event) => setSortBy(event.target.value)}
            >
              <option value="featured">Featured</option>
              <option value="newest">Newest</option>
              <option value="name">Name (A–Z)</option>
            </select>
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
              <Link to={`/destinations/${destination.id}`} className="destination-card" key={destination.id}>
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
              </Link>
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
      </div>
    } />

    <Route
      path="/destinations/:id"
      element={<DestinationDetails />}
    />
  </Routes>
)
}

export default App
