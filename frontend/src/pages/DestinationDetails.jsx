import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getDestinationById } from '../services/destinationService'

function DestinationDetails() {
  const { id } = useParams()

  const [destination, setDestination] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchDestination = async () => {
      setLoading(true)

      try {
        const response = await getDestinationById(id)
        setDestination(response.data)
      } catch (error) {
        console.error('Error fetching destination:', error)
        setDestination(null)
      } finally {
        setLoading(false)
      }
    }

    fetchDestination()
  }, [id])

  if (loading) {
    return <p>Loading destination...</p>
  }

  if (!destination) {
    return <p>Destination not found.</p>
  }

  return (
    <div>
      <h1>{destination.name}</h1>

      <img
        src={
          destination.image
            ? `http://127.0.0.1:8000${destination.image}`
            : 'https://placehold.co/600x400?text=Destination'
        }
        alt={destination.name}
        style={{ width: '100%', maxWidth: '700px' }}
      />

      <p>
        {destination.location}, {destination.state}
      </p>

      <p>{destination.description}</p>

      <h3>Categories</h3>

      <ul>
        {destination.categories?.map((category) => (
          <li key={category.id}>{category.name}</li>
        ))}
      </ul>
    </div>
  )
}

export default DestinationDetails
