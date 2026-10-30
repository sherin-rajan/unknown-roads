import api from '../api/axios'

export const changePassword = async (passwordData) => {
  const response = await api.post(
    'accounts/change-password/',
    passwordData
  )

  return response.data
}
