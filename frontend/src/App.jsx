import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import DestinationDetails from './pages/DestinationDetails'
import Register from './pages/Register'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import ProtectedRoute from './components/ProtectedRoute'
import Profile from './pages/Profile'
import Favorites from './pages/Favorites'
import ChangePassword from './pages/ChangePassword'
import './App.css'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />

      <Route
        path="/destinations/:id"
        element={<DestinationDetails />}
      />

      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />

      {/* Protected customer pages */}
      <Route element={<ProtectedRoute />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />
        <Route path="/favorites" element={<Favorites />} />
        <Route path="/change-password" element={<ChangePassword />} />
      </Route>
    </Routes>
  )
}

export default App
