import api from '../api/axios'

// Get the logged-in customer's profile
export const getProfile = async () => {
  const response = await api.get('accounts/profile/')
  return response.data
}

// Update the logged-in customer's profile
export const updateProfile = async (profileData) => {
  const response = await api.patch(
    'accounts/profile/',
    profileData
  )

  return response.data
}
