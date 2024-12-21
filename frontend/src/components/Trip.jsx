import React, { useEffect, useState } from 'react';
import { Box, Button } from '@mui/material';
import AxiosInstance from './AxiosInstance';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const placeholderImage = 'https://www.travelturtle.world/wp-content/uploads/2024/03/6585d85934a171a9a052c170_traveling-based-on-fare-deals.jpeg';

const Trip = () => {
    const [trips, setTrips] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetchTrips();
    }, []);

    const fetchTrips = async () => {
        try {
            const response = await AxiosInstance.get('api/trips/');
            const tripsData = response.data;

            // Fetch image URLs for trips with the placeholder image URL
            const updatedTrips = await Promise.all(tripsData.map(async (trip) => {
                if (trip.image_url === placeholderImage) {
                    const imageUrl = await fetchImageUrlForTrip(trip.place);
                    trip.image_url = imageUrl;

                    // Optionally, update the trip in the backend with the new image URL
                    await AxiosInstance.patch(`api/trips/${trip.id}/`, { image_url: imageUrl });
                }
                return trip;
            }));

            setTrips(updatedTrips);
        } catch (error) {
            console.error('Error fetching trips:', error);
        }
    };

    const fetchImageUrlForTrip = async (place) => {
        try {
            const response = await AxiosInstance.get(`/api/fetch-image-url-for-trip/`, { params: { place } });
            if (response.data && response.data.image_url) {
                return response.data.image_url;
            }
            return placeholderImage;
        } catch (error) {
            console.error('Error fetching image URL for trip:', error);
            return placeholderImage;
        }
    };

    const handleViewPlaces = (tripId) => {
        navigate(`/places/${tripId}`);
    };

    return (
        <Box className="myBackground">
            <Box className="centeredContent">
                <div className="title">Trip List</div>
                {trips.map(trip => (
                    <Box key={trip.id} className="tripBox">
                        <img src={trip.image_url || placeholderImage} alt={trip.place} className="tripImage" />
                        <div className="tripDetails">
                            <div>{trip.place} - {trip.starting_date}</div>
                        </div>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={() => handleViewPlaces(trip.id)}
                            className="viewButton"
                        >
                            View Places
                        </Button>
                    </Box>
                ))}
            </Box>
        </Box>
    );
};

export default Trip;