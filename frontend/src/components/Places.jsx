import React, { useEffect, useState } from 'react';
import { Box, Button, TextField, Checkbox, FormControlLabel, Typography } from '@mui/material';
import AxiosInstance from './AxiosInstance';
import { useParams } from 'react-router-dom';
import '../App.css';

const placeholderImage = 'https://www.travelturtle.world/wp-content/uploads/2024/03/6585d85934a171a9a052c170_traveling-based-on-fare-deals.jpeg';

const Places = () => {
    const { tripId } = useParams();
    const [places, setPlaces] = useState([]);
    const [newPlace, setNewPlace] = useState('');
    const [trip, setTrip] = useState(null);

    useEffect(() => {
        fetchTrip();
        fetchPlaces();
    }, [tripId]);

    const fetchTrip = async () => {
        try {
            const response = await AxiosInstance.get(`api/trips/${tripId}/`);
            setTrip(response.data);
        } catch (error) {
            console.error('Error fetching trip:', error);
        }
    };

    const fetchPlaces = async () => {
        try {
            const response = await AxiosInstance.get(`api/trips/${tripId}/`);
            const placesData = response.data.places;

            const updatedPlaces = await Promise.all(placesData.map(async (place) => {
                if (place.image_url === placeholderImage) {
                    const imageUrl = await fetchImageUrl(place.name, tripId);
                    place.image_url = imageUrl;

                    await AxiosInstance.patch(`api/places/${place.id}/`, { image_url: imageUrl });
                }
                return place;
            }));

            setPlaces(updatedPlaces);
        } catch (error) {
            console.error('Error fetching places:', error);
        }
    };

    const fetchImageUrl = async (placeName, tripId) => {
        try {
            const response = await AxiosInstance.get(`/api/fetch-image-url/`, { params: { place_name: placeName, trip_id: tripId } });
            if (response.data && response.data.image_url) {
                return response.data.image_url;
            }
            return placeholderImage;
        } catch (error) {
            console.error('Error fetching image URL:', error);
            return placeholderImage;
        }
    };

    const handleAddPlace = async () => {
        let imageUrl = placeholderImage;
        try {
            imageUrl = await fetchImageUrl(newPlace, tripId);
        } catch (error) {
            if (error.response && error.response.status === 429) {
                console.error('Rate limit exceeded. Using placeholder image.');
            } else {
                console.error('Error fetching image URL:', error);
            }
        }

        try {
            await AxiosInstance.post('api/places/', { name: newPlace, trip: tripId, image_url: imageUrl });
            setNewPlace('');
            fetchPlaces();
        } catch (error) {
            console.error('Error adding place:', error);
        }
    };

    const handleRemovePlace = (placeId, event) => {
        event.stopPropagation();
        AxiosInstance.delete(`api/places/${placeId}/`)
            .then(() => {
                fetchPlaces();
            })
            .catch(error => {
                console.error('Error removing place:', error);
            });
    };

    const handleToggleVisited = (placeId, visited, event) => {
        event.stopPropagation();
        AxiosInstance.patch(`api/places/${placeId}/`, { visited: !visited })
            .then(() => {
                fetchPlaces();
            })
            .catch(error => {
                console.error('Error updating place:', error);
            });
    };

    const handlePlaceClick = (place) => {
        const cityName = trip ? trip.place : '';
        const query = encodeURIComponent(`${place.name} in ${cityName}`);
        const url = `https://www.google.com/search?q=${query}`;
        window.open(url, '_blank');
    };

    return (
        <Box className="myBackground">
            <Box className="centeredContent">
                <Typography variant="h4" gutterBottom>
                    Places in my Trip
                </Typography>
                {places.map(place => (
                    <Box className="placeBox" key={place.id} onClick={() => handlePlaceClick(place)}>
                        <img src={place.image_url || placeholderImage} alt={place.name} className="placeImage" />
                        <Typography className="placeName">{place.name}</Typography>
                        <Box className="buttonGroup">
                            <FormControlLabel
                                control={
                                    <Checkbox
                                        checked={place.visited}
                                        onClick={(event) => event.stopPropagation()}
                                        onChange={(event) => handleToggleVisited(place.id, place.visited, event)}
                                        className="visitedCheckbox"
                                    />
                                }
                                label="Visited"
                            />
                            <Button
                                variant="contained"
                                color="secondary"
                                onClick={(event) => {
                                    event.stopPropagation();
                                    handleRemovePlace(place.id, event);
                                }}
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
