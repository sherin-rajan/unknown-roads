import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import Navbar from '../components/Navbar'
import { changePassword } from '../services/passwordService'

function ChangePassword() {
    const navigate = useNavigate()

    const [formData, setFormData] = useState({
        current_password: '',
        new_password: '',
        confirm_password: '',
    })

    const [showPasswords, setShowPasswords] = useState({
        current: false,
        new: false,
        confirm: false,
    })

    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        })
    }

    const togglePassword = (field) => {
        setShowPasswords({
            ...showPasswords,
            [field]: !showPasswords[field],
        })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')

        // Check whether all fields are filled
        if (
            !formData.current_password ||
            !formData.new_password ||
            !formData.confirm_password
        ) {
            setError('Please fill in all fields.')
            return
        }

        // Check minimum password length
        if (formData.new_password.length < 8) {
            setError('Your new password must contain at least 8 characters.')
            return
        }

        // Check whether passwords match
        if (formData.new_password !== formData.confirm_password) {
            setError('New password and confirm password do not match.')
            return
        }

        // Check whether the new password is different
        if (formData.current_password === formData.new_password) {
            setError(
                'Your new password must be different from your current password.'
            )
            return
        }

        try {
            setLoading(true)

            await changePassword({
                old_password: formData.current_password,
                new_password: formData.new_password,
                confirm_password: formData.confirm_password,
            })

            // Navigate only after a successful password update
            navigate('/dashboard')

        } catch (err) {
            console.error('Password change failed:', err)

            const responseData = err.response?.data

            if (responseData) {
                const message = Object.values(responseData)
                    .flat()
                    .join(' ')

                setError(message || 'Unable to change your password.')
            } else {
                setError('Something went wrong. Please try again.')
            }

        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="app">
            <Navbar />

            <main className="change-password-page">
                <section className="change-password-container">

                    <div className="change-password-heading">
                        <p className="section-label">ACCOUNT SECURITY</p>
                        <h1>Change Password</h1>
                        <p>
                            Keep your account secure by updating your password regularly.
                        </p>
                    </div>

                    {error && (
                        <div className="password-error">
                            {error}
                        </div>
                    )}

                    <form
                        onSubmit={handleSubmit}
                        className="change-password-form"
                    >

                        {/* Current Password */}
                        <div className="password-field">
                            <label htmlFor="current_password">
                                Current Password
                            </label>

                            <div className="password-input-wrapper">
                                <input
                                    type={showPasswords.current ? 'text' : 'password'}
                                    id="current_password"
                                    name="current_password"
                                    value={formData.current_password}
                                    onChange={handleChange}
                                    autoComplete="current-password"
                                />

                                <button
                                    type="button"
                                    onClick={() => togglePassword('current')}
                                    className="password-toggle"
                                >
                                    {showPasswords.current ? 'Hide' : 'Show'}
                                </button>
                            </div>
                        </div>

                        {/* New Password */}
                        <div className="password-field">
                            <label htmlFor="new_password">
                                New Password
                            </label>

                            <div className="password-input-wrapper">
                                <input
                                    type={showPasswords.new ? 'text' : 'password'}
                                    id="new_password"
                                    name="new_password"
                                    value={formData.new_password}
                                    onChange={handleChange}
                                    autoComplete="new-password"
                                />

                                <button
                                    type="button"
                                    onClick={() => togglePassword('new')}
                                    className="password-toggle"
                                >
                                    {showPasswords.new ? 'Hide' : 'Show'}
                                </button>
                            </div>
                        </div>

                        {/* Confirm New Password */}
                        <div className="password-field">
                            <label htmlFor="confirm_password">
                                Confirm New Password
                            </label>

                            <div className="password-input-wrapper">
                                <input
                                    type={showPasswords.confirm ? 'text' : 'password'}
                                    id="confirm_password"
                                    name="confirm_password"
                                    value={formData.confirm_password}
                                    onChange={handleChange}
                                    autoComplete="new-password"
                                />

                                <button
                                    type="button"
                                    onClick={() => togglePassword('confirm')}
                                    className="password-toggle"
                                >
                                    {showPasswords.confirm ? 'Hide' : 'Show'}
                                </button>
                            </div>
                        </div>

                        {/* Submit Button */}
                        <button
                            type="submit"
                            className="change-password-button"
                            disabled={loading}
                        >
                            {loading ? 'Updating...' : 'Update Password'}
                        </button>

                    </form>

                    <Link
                        to="/dashboard"
                        className="password-back-link"
                    >
                        Back to Dashboard
                    </Link>

                </section>
            </main>
        </div>
    )
}

export default ChangePassword
