import React, { useEffect, useState } from 'react';
import { Box, Button, TextField, Checkbox, FormControlLabel, Typography } from '@mui/material';
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
        AxiosInstance.post('api/places/', { name: newPlace, trip: tripId })
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
            <Box className="centeredContent">
                <Typography variant="h4" gutterBottom>
                    Places in my Trip
                </Typography>
                {places.map(place => (
                    <Box className="placeBox" key={place.id}>
                        <Typography className="placeName">{place.name}</Typography>
                        <Box className="buttonGroup">
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={place.visited}
                                        onChange={() => handleToggleVisited(place.id, place.visited)}
                                        className="visitedCheckbox"
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
                    </Box>
                ))}
                <Box className="textFieldContainer">
                    <TextField
                        label="New Place"
                        value={newPlace}
                        onChange={(e) => setNewPlace(e.target.value)}
                        fullWidth
                    />
                    <Button
                        variant="contained"
                        className="addButton"
                        onClick={handleAddPlace}
                    >
                        Add Place
                    </Button>
                </Box>
            </Box>
        </Box>
    );
};

export default Places;