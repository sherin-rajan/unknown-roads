function DestinationFilters({
  categories,
  selectedCategory,
  setSelectedCategory,
  searchTerm,
  setSearchTerm,
  sortBy,
  setSortBy,
  setPage,
}) {
  const handleSearchChange = (value) => {
    setSearchTerm(value)
    setPage(1)
  }

  const handleCategoryChange = (categoryName) => {
    setSelectedCategory(categoryName)
    setPage(1)
  }

  const handleSortChange = (value) => {
    setSortBy(value)
    setPage(1)
  }

  return (
    <>
      <div className="destination-search">
        <input
          type="text"
          placeholder="Search destinations by name, state, or location..."
          value={searchTerm}
          onChange={(event) => handleSearchChange(event.target.value)}
        />
      </div>

      <div className="sort-control">
        <label htmlFor="sortBy">Sort by:</label>

        <select
          id="sortBy"
          value={sortBy}
          onChange={(event) => handleSortChange(event.target.value)}
        >
          <option value="featured">Featured</option>
          <option value="newest">Newest</option>
          <option value="name">Name (A–Z)</option>
        </select>
      </div>

      <div className="category-filters">
        <button
          type="button"
          className={selectedCategory === '' ? 'active' : ''}
          onClick={() => handleCategoryChange('')}
        >
          All Destinations
        </button>

        {categories.map((category) => (
          <button
            type="button"
            key={category.id}
            className={
              selectedCategory === category.name ? 'active' : ''
            }
            onClick={() => handleCategoryChange(category.name)}
          >
            {category.name}
          </button>
        ))}
      </div>
    </>
  )
}

export default DestinationFilters
