import api from '../api/axios'

export const registerUser = async (userData) => {
  const response = await api.post('accounts/register/', userData)
  return response.data
}

export const loginUser = async (credentials) => {
  const response = await api.post('accounts/login/', credentials)

  sessionStorage.setItem('access', response.data.access)
  sessionStorage.setItem('refresh', response.data.refresh)

  return response.data
}

export const getCurrentUser = async () => {
  const response = await api.get('accounts/me/')
  return response.data
}

export const logoutUser = async () => {
  const refresh = sessionStorage.getItem('refresh')

  try {
    if (refresh) {
      await api.post('accounts/logout/', { refresh })
    }
  } finally {
    sessionStorage.removeItem('access')
    sessionStorage.removeItem('refresh')
  }
}
