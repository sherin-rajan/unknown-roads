import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getDestinations } from '../services/destinationService'
import { getCategories } from '../services/categoryService'

function Home() {
    const [destinations, setDestinations] = useState([])
    const [categories, setCategories] = useState([])
    const [loading, setLoading] = useState(true)
    const [categoriesLoading, setCategoriesLoading] = useState(true)
    const [selectedCategory, setSelectedCategory] = useState('')
    const [searchTerm, setSearchTerm] = useState('')
    const [debouncedSearchTerm, setDebouncedSearchTerm] = useState('')
    const [sortBy, setSortBy] = useState('featured')
    const [error, setError] = useState('')
    const [categoryError, setCategoryError] = useState('')
    const [page, setPage] = useState(1)
    const [totalCount, setTotalCount] = useState(0)

    useEffect(() => {
        const fetchCategories = async () => {
            setCategoriesLoading(true)
            setCategoryError('')

            try {
                const response = await getCategories()
                const data = response.data
                setCategories(Array.isArray(data) ? data : data.results ?? [])
            } catch (error) {
                console.error('Error fetching categories:', error)
                setCategoryError('Unable to load categories. Please try again.')
            } finally {
                setCategoriesLoading(false)
            }
        }

        fetchCategories()
    }, [])

    useEffect(() => {
        const timer = setTimeout(() => {
            setDebouncedSearchTerm(searchTerm)
        }, 400)

        return () => clearTimeout(timer)
    }, [searchTerm])

    useEffect(() => {
        const fetchDestinations = async () => {
            setLoading(true)
            setError('')

            try {
                const params = {
                    ordering: sortBy,
                    page,
                }

                if (selectedCategory) {
                    params.category = selectedCategory
                }

                if (debouncedSearchTerm.trim()) {
                    params.search = debouncedSearchTerm.trim()
                }

                const response = await getDestinations(params)

                setDestinations(response.data.results)
                setTotalCount(response.data.count)
            } catch (error) {
                console.error('Error fetching destinations:', error)
                setError('Unable to load destinations. Please try again.')
                setDestinations([])
                setTotalCount(0)
            } finally {
                setLoading(false)
            }
        }

        fetchDestinations()
    }, [selectedCategory, debouncedSearchTerm, sortBy, page])

    const totalPages = Math.ceil(totalCount / 5)

    const clearFilters = () => {
        setSearchTerm('')
        setDebouncedSearchTerm('')
        setSelectedCategory('')
        setSortBy('featured')
        setPage(1)
    }

    return (
        <div className="app">
            <nav className="navbar">
                <h1 className="logo">
                    Unknown Roads<span>.</span>
                </h1>

                <div className="nav-links">
                    <Link to="/">Home</Link>
                    <a href="#destinations">Destinations</a>
                    <a href="#about">About</a>
                </div>

                <a href="#destinations" className="nav-button">
                    Explore Trips
                </a>
            </nav>

            <main>
                <section className="hero">
                    <p className="hero-tagline">
                        YOUR NEXT ADVENTURE STARTS HERE
                    </p>

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

                <section className="intro" id="about">
                    <p className="section-label">EXPLORE THE WORLD</p>
                    <h2>Where will your next journey take you?</h2>
                    <p>
                        From peaceful escapes to adventurous trails,
                        your next unforgettable experience awaits.
                    </p>
                </section>

                <section className="destinations-section" id="destinations">
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
                            onChange={(event) => {
                                setSearchTerm(event.target.value)
                                setPage(1)
                            }}
                        />
                    </div>

                    <div className="sort-control">
                        <label htmlFor="sortBy">Sort by:</label>

                        <select
                            id="sortBy"
                            value={sortBy}
                            onChange={(event) => {
                                setSortBy(event.target.value)
                                setPage(1)
                            }}
                        >
                            <option value="featured">Featured</option>
                            <option value="newest">Newest</option>
                            <option value="name">Name (A–Z)</option>
                        </select>
                    </div>

                    <div className="category-filters">
                        <button
                            className={selectedCategory === '' ? 'active' : ''}
                            onClick={() => {
                                setSelectedCategory('')
                                setPage(1)
                            }}
                        >
                            All Destinations
                        </button>

                        {categories.map((category) => (
                            <button
                                key={category.id}
                                className={
                                    selectedCategory === category.name ? 'active' : ''
                                }
                                onClick={() => {
                                    setSelectedCategory(category.name)
                                    setPage(1)
                                }}
                            >
                                {category.name}
                            </button>
                        ))}
                    </div>

                    {categoryError && (
                        <p className="error-message">{categoryError}</p>
                    )}

                    {categoriesLoading && (
                        <p className="empty-message">Loading categories...</p>
                    )}

                    {error ? (
                        <p className="error-message">{error}</p>
                    ) : loading ? (
                        <p className="empty-message">Loading destinations...</p>
                    ) : destinations.length === 0 ? (
                        <div className="empty-state">
                            <h3>No destinations found</h3>
                            <p>
                                We couldn't find any destinations matching your search.
                                Try changing your search or filters to discover more places.
                            </p>

                            <button
                                className="clear-filters-button"
                                onClick={clearFilters}
                            >
                                Clear Search & Filters
                            </button>
                        </div>
                    ) : (
                        <div className="destination-grid">
                            {destinations.map((destination) => (
                                <Link
                                    to={`/destinations/${destination.id}`}
                                    className="destination-card"
                                    key={destination.id}
                                >
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
                    )}

                    {!error && !loading && totalCount > 5 && (
                        <div className="pagination">
                            <button
                                onClick={() =>
                                    setPage((currentPage) => currentPage - 1)
                                }
                                disabled={page === 1}
                            >
                                ← Previous
                            </button>

                            <span>
                                Page {page} of {totalPages}
                            </span>

                            <button
                                onClick={() =>
                                    setPage((currentPage) => currentPage + 1)
                                }
                                disabled={page >= totalPages}
                            >
                                Next →
                            </button>
                        </div>
                    )}
                </section>
            </main>
        </div>
    )
}

export default Home
