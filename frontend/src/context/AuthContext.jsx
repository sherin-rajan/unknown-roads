import { createContext, useContext, useEffect, useState } from 'react'
import { getCurrentUser, loginUser, logoutUser } from '../services/authService'

const AuthContext = createContext()

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Check whether a customer is already logged in
  useEffect(() => {
    const checkAuth = async () => {
      const access = sessionStorage.getItem('access')

      if (!access) {
        setLoading(false)
        return
      }

      try {
        const currentUser = await getCurrentUser()
        setUser(currentUser)
      } catch (error) {
        console.error('Authentication check failed:', error)
        setUser(null)
      } finally {
        setLoading(false)
      }
    }

    checkAuth()
  }, [])

  // Log in a customer
  const login = async (credentials) => {
    await loginUser(credentials)

    const currentUser = await getCurrentUser()
    setUser(currentUser)

    return currentUser
  }

  // Log out a customer
  const logout = async () => {
    try {
      await logoutUser()
    } finally {
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider
      value={{ user, loading, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  )
}

// Custom hook to access authentication
export function useAuth() {
  return useContext(AuthContext)
}
