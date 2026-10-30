
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import Navbar from '../components/Navbar'
import { getProfile, updateProfile } from '../services/profileService'
import { getCategories } from '../services/categoryService'

function Profile() {
  const [profile, setProfile] = useState(null)
  const [formData, setFormData] = useState({})
  const [username, setUsername] = useState('')
  const [categories, setCategories] = useState([])

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const getFormData = (data) => ({
    first_name: data.first_name || '',
    last_name: data.last_name || '',
    email: data.email || '',
    phone_number: data.phone_number || '',
    date_of_birth: data.date_of_birth || '',
    place: data.place || '',
    preferred_categories: data.preferred_categories || [],
  })

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const [profileResponse, categoryResponse] = await Promise.all([
          getProfile(),
          getCategories(),
        ])

        const categoryData = categoryResponse.data
        const loadedCategories = Array.isArray(categoryData)
          ? categoryData
          : categoryData.results || []

        setUsername(profileResponse.username || '')
        setCategories(loadedCategories)

        const initialData = getFormData(profileResponse)
        setProfile(initialData)
        setFormData(initialData)
      } catch (err) {
        console.error('Profile loading failed:', err)
        setError('Unable to load your profile. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    loadProfile()
  }, [])

  const handleChange = (event) => {
    const { name, value } = event.target

    setFormData((previous) => ({
      ...previous,
      [name]: value,
    }))

    setError('')
    setSuccess('')
  }

  const handleCategoryChange = (categoryId) => {
    setFormData((previous) => {
      const selected = previous.preferred_categories

      const updated = selected.includes(categoryId)
        ? selected.filter((id) => id !== categoryId)
        : [...selected, categoryId]

      return {
        ...previous,
        preferred_categories: updated,
      }
    })

    setError('')
    setSuccess('')
  }

  const handleEdit = () => {
    setFormData({ ...profile })
    setIsEditing(true)
    setError('')
    setSuccess('')
  }

  const handleCancel = () => {
    setFormData({ ...profile })
    setIsEditing(false)
    setError('')
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    setSaving(true)
    setError('')
    setSuccess('')

    try {
      const updatedProfile = await updateProfile(formData)
      const updatedData = getFormData(updatedProfile)

      setProfile(updatedData)
      setFormData(updatedData)
      setIsEditing(false)
      setSuccess('Your profile has been updated successfully.')
    } catch (err) {
      console.error('Profile update failed:', err)

      const errors = err.response?.data

      if (errors && typeof errors === 'object') {
        const messages = Object.entries(errors)
          .map(([field, messages]) => {
            const message = Array.isArray(messages)
              ? messages.join(', ')
              : messages

            return `${field}: ${message}`
          })
          .join(' | ')

        setError(messages || 'Unable to update your profile.')
      } else {
        setError('Unable to update your profile. Please try again.')
      }
    } finally {
      setSaving(false)
    }
  }

  const preferredCategories = categories.filter((category) =>
    profile?.preferred_categories.includes(category.id)
  )

  if (loading) {
    return (
      <div className="app">
        <Navbar />
        <p className="empty-message">Loading your profile...</p>
      </div>
    )
  }

  if (!profile) {
    return (
      <div className="app">
        <Navbar />
        <p className="form-error">{error}</p>
      </div>
    )
  }

  return (
    <div className="app">
      <Navbar />

      <main className="profile-page">
        <div className="profile-heading">
          <p className="section-label">YOUR ACCOUNT</p>
          <h1>My Profile</h1>
          <p>Manage your personal information and travel preferences.</p>
        </div>

        {success && <p className="form-success">{success}</p>}
        {error && <p className="form-error">{error}</p>}

        {!isEditing ? (
          <section className="profile-view">
            <div className="profile-view-header">
              <div>
                <h2>{profile.first_name || username} {profile.last_name}</h2>
                <p>@{username}</p>
              </div>

              <button type="button" onClick={handleEdit}>
                Edit Profile
              </button>
            </div>

            <div className="profile-information">
              <h3>Personal Information</h3>

              <div className="profile-info-grid">
                <div>
                  <span>First Name</span>
                  <p>{profile.first_name || 'Not provided'}</p>
                </div>

                <div>
                  <span>Last Name</span>
                  <p>{profile.last_name || 'Not provided'}</p>
                </div>

                <div>
                  <span>Email Address</span>
                  <p>{profile.email || 'Not provided'}</p>
                </div>

                <div>
                  <span>Phone Number</span>
                  <p>{profile.phone_number || 'Not provided'}</p>
                </div>

                <div>
                  <span>Date of Birth</span>
                  <p>{profile.date_of_birth || 'Not provided'}</p>
                </div>

                <div>
                  <span>Place</span>
                  <p>{profile.place || 'Not provided'}</p>
                </div>
              </div>
            </div>

            <div className="profile-information">
              <h3>Preferred Travel Categories</h3>

              {preferredCategories.length > 0 ? (
                <div className="profile-category-list">
                  {preferredCategories.map((category) => (
                    <span
                      key={category.id}
                      className="profile-category-display"
                    >
                      {category.name}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="profile-no-preferences">
                  You haven't selected any preferred categories yet.
                </p>
              )}
            </div>

            <Link to="/dashboard" className="profile-back-link">
              Back to Dashboard
            </Link>
          </section>
        ) : (
          <form className="profile-form" onSubmit={handleSubmit}>
            <div className="profile-form-header">
              <h2>Edit Your Information</h2>
              <p>Update your personal details and travel preferences.</p>
            </div>

            <div className="profile-field">
              <label>Username</label>
              <input type="text" value={username} disabled />
              <small>Your username cannot be changed.</small>
            </div>

            <div className="profile-form-grid">
              <div className="profile-field">
                <label htmlFor="first_name">First Name</label>
                <input
                  id="first_name"
                  name="first_name"
                  type="text"
                  value={formData.first_name}
                  onChange={handleChange}
                />
              </div>

              <div className="profile-field">
                <label htmlFor="last_name">Last Name</label>
                <input
                  id="last_name"
                  name="last_name"
                  type="text"
                  value={formData.last_name}
                  onChange={handleChange}
                />
              </div>

              <div className="profile-field">
                <label htmlFor="email">Email Address</label>
                <input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>

              <div className="profile-field">
                <label htmlFor="phone_number">Phone Number</label>
                <input
                  id="phone_number"
                  name="phone_number"
                  type="tel"
                  value={formData.phone_number}
                  onChange={handleChange}
                  placeholder="e.g. +919876543210"
                />
              </div>

              <div className="profile-field">
                <label htmlFor="date_of_birth">Date of Birth</label>
                <input
                  id="date_of_birth"
                  name="date_of_birth"
                  type="date"
                  value={formData.date_of_birth}
                  onChange={handleChange}
                />
              </div>

              <div className="profile-field">
                <label htmlFor="place">Place</label>
                <input
                  id="place"
                  name="place"
                  type="text"
                  value={formData.place}
                  onChange={handleChange}
                  placeholder="Your city or town"
                />
              </div>
            </div>

            <div className="profile-field profile-categories">
              <label>Preferred Travel Categories</label>
              <p>Select the types of trips you are interested in.</p>

              <div className="profile-category-list">
                {categories.map((category) => (
                  <label
                    key={category.id}
                    className="profile-category-option"
                  >
                    <input
                      type="checkbox"
                      checked={formData.preferred_categories.includes(category.id)}
                      onChange={() => handleCategoryChange(category.id)}
                    />
                    <span>{category.name}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="profile-actions">
              <button type="submit" disabled={saving}>
                {saving ? 'Saving...' : 'Save Changes'}
              </button>

              <button
                type="button"
                className="profile-cancel-button"
                onClick={handleCancel}
                disabled={saving}
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </main>
    </div>
  )
}

export default Profile
