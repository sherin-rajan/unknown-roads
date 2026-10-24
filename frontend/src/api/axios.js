import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:8000/api/'

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
})

api.interceptors.request.use(
  (config) => {
    const access = sessionStorage.getItem('access')

    if (access) {
      config.headers.Authorization = `Bearer ${access}`
    }

    return config
  },
  (error) => Promise.reject(error)
)

let refreshPromise = null

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (
      error.response?.status !== 401 ||
      !originalRequest ||
      originalRequest._retry ||
      originalRequest.url?.includes('accounts/login/') ||
      originalRequest.url?.includes('accounts/token/refresh/') ||
      originalRequest.url?.includes('accounts/register/')
    ) {
      return Promise.reject(error)
    }

    const refresh = sessionStorage.getItem('refresh')

    if (!refresh) {
      sessionStorage.removeItem('access')
      return Promise.reject(error)
    }

    originalRequest._retry = true

    try {
      if (!refreshPromise) {
        refreshPromise = axios
          .post(`${BASE_URL}accounts/token/refresh/`, { refresh })
          .then((response) => {
            sessionStorage.setItem('access', response.data.access)

            if (response.data.refresh) {
              sessionStorage.setItem('refresh', response.data.refresh)
            }

            return response.data.access
          })
          .finally(() => {
            refreshPromise = null
          })
      }

      const newAccess = await refreshPromise

      originalRequest.headers.Authorization = `Bearer ${newAccess}`

      return api(originalRequest)
    } catch (refreshError) {
      sessionStorage.removeItem('access')
      sessionStorage.removeItem('refresh')

      return Promise.reject(refreshError)
    }
  }
)

export default api
