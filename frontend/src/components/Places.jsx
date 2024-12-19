import React, { useEffect, useState } from 'react';
import { Box, Button, TextField, Checkbox, FormControlLabel } from '@mui/material';
import AxiosInstance from './AxiosInstance';
import { useParams } from 'react-router-dom';
import '../App.css';

const Places = () => {
    const { tripId } = useParams();
    const [places, setPlaces] = useState([]);
    const [newPlace, setNewPlace] = useState('');

    useEffect(() => {
        fetchPlaces();
    }, [tripId]);

    const fetchPlaces = () => {
        AxiosInstance.get(`api/trips/${tripId}/`)
            .then(response => {
                setPlaces(response.data.places);
            })
            .catch(error => {
                console.error('Error fetching places:', error);
            });
    };

    const handleAddPlace = () => {
        AxiosInstance.post('api/places/', { name: newPlace, trip_id: tripId })
            .then(() => {
                setNewPlace('');
                fetchPlaces();
            })
            .catch(error => {
                console.error('Error adding place:', error);
            });
    };

    const handleRemovePlace = (placeId) => {
        AxiosInstance.delete(`api/places/${placeId}/`)
            .then(() => {
                fetchPlaces();
            })
            .catch(error => {
                console.error('Error removing place:', error);
            });
    };

    const handleToggleVisited = (placeId, visited) => {
        AxiosInstance.patch(`api/places/${placeId}/`, { visited: !visited })
            .then(() => {
                fetchPlaces();
            })
            .catch(error => {
                console.error('Error updating place:', error);
            });
    };

    return (
        <Box className="myBackground">
            <Box className="centeredContent" sx={{ flexDirection: 'column', gap: 2 }}>
                {places.map(place => (
                    <Box key={place.id} sx={{ marginBottom: '16px' }}>
                        <div>{place.name}</div>
                        <FormControlLabel
                            control={
                                <Checkbox
                                    checked={place.visited}
                                    onChange={() => handleToggleVisited(place.id, place.visited)}
                                />
                            }
                            label="Visited"
                        />
                        <Button
                            variant="contained"
                            color="secondary"
                            onClick={() => handleRemovePlace(place.id)}
                        >
                            Remove
                        </Button>
                    </Box>
                ))}
                <Box sx={{ marginTop: '16px', width: '100%' }}>
                    <TextField
                        label="New Place"
                        value={newPlace}
                        onChange={(e) => setNewPlace(e.target.value)}
                        fullWidth
                    />
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={handleAddPlace}
                        sx={{ marginTop: '8px' }}
                    >
                        Add Place
                    </Button>
                </Box>
            </Box>
        </Box>
    );
};

export default Places;