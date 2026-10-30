import api from '../api/axios'

// Get all saved destinations
export const getFavorites = async () => {
  const response = await api.get('accounts/favorites/')
  return response.data
}

// Add a destination to favorites
export const addFavorite = async (destinationId) => {
  const response = await api.post('accounts/favorites/', {
    destination: destinationId,
  })
  return response.data
}

// Remove a destination from favorites
export const removeFavorite = async (favoriteId) => {
  const response = await api.delete(`accounts/favorites/${favoriteId}/`)
  return response.data
}
