import React, { useEffect, useState } from 'react';
import { Box, Button } from '@mui/material';
import AxiosInstance from './AxiosInstance';
import { useNavigate } from 'react-router-dom';
import '../App.css';

const Trip = () => {
    const [trips, setTrips] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        AxiosInstance.get('api/trips/')
            .then(response => {
                setTrips(response.data);
            })
            .catch(error => {
                console.error('Error fetching trips:', error);
            });
    }, []);

    const handleViewPlaces = (tripId) => {
        navigate(`/places/${tripId}`);
    };

    return (
        <Box className="myBackground">
            <Box className="centeredContent" sx={{ flexDirection: 'column', gap: 2 }}>
                {trips.map(trip => (
                    <Box key={trip.id} sx={{ marginBottom: '16px' }}>
                        <div>{trip.place} - {trip.starting_date}</div>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={() => handleViewPlaces(trip.id)}
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