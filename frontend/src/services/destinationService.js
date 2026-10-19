import api from '../api/axios'

export const getDestinations = (params = {}) => {
  return api.get('destinations/', { params })
}

export const getDestinationById = (id) => {
  return api.get(`destinations/${id}/`)
}
