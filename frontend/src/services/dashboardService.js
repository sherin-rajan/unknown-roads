import api from '../api/axios'

export const getCustomerDashboard = async () => {
  const response = await api.get('accounts/customer-dashboard/')
  return response.data
}

export const getManagerDashboard = async () => {
  const response = await api.get('accounts/manager-dashboard/')
  return response.data
}