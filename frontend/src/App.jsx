import { useEffect, useState } from 'react'
import './App.css'

function App() {
  const [destinations, setDestinations] = useState([])

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/destinations/')
      .then((response) => response.json())
      .then((data) => {
        setDestinations(data.results)
      })
      .catch((error) => {
        console.error('Error fetching destinations:', error)
      })
  }, [])
  
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
      </main>
    </div>
  )
}

export default App
