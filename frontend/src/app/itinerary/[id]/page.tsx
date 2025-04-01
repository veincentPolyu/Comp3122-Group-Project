'use client';

import React, { useCallback } from 'react';
import { Box, Button, Checkbox, Container, Dialog, DialogActions, DialogContent, DialogTitle, Divider, FormControlLabel, FormGroup, List, ListItem, ListItemText, Typography } from '@mui/material';
import Itinerary from '../../../components/Itinerary';
import { Location } from '../../../types/location';
import TravelInfoExtrationURLInput from '../../../components/TravelInfoExtrationURLInput';
import MapComponent from "../../../components/Map";

const dummyLocations: Location[] = [
    {
      id: '1',
      name: 'Eiffel Tower',
      address: 'Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France',
      category: 'attraction',
      coordinates: { lat: 48.8584, lng: 2.2945 },
      business_hours: ['09:00-00:00'],
      rating: 4.7,
      price_level: 2,
      photos: ['https://i.pinimg.com/736x/be/08/d9/be08d9d7b0d57f9102f8d6ec3f9e2a0e.jpg'],
      description: 'Iconic iron lattice tower on the Champ de Mars in Paris',
      tags: ['landmark', 'tourist attraction', 'observation deck'],
      created_at: '2023-01-01T00:00:00Z'
    },
    {
      id: '2',
      name: 'Louvre Museum',
      address: 'Rue de Rivoli, 75001 Paris, France',
      category: 'attraction',
      coordinates: { lat: 48.8606, lng: 2.3376 },
      business_hours: ['09:00-18:00'],
      rating: 4.8,
      price_level: 3,
      photos: ['https://i.pinimg.com/736x/a2/74/18/a27418842ee3199ec3dcf9540312847d.jpg'],
      description: 'World\'s largest art museum and historic monument',
      tags: ['art', 'history', 'museum'],
      created_at: '2023-01-01T00:00:00Z'
    },
    // Adding a hotel
    {
      id: '3',
      name: 'Hotel Plaza Athenee',
      address: '25 Avenue Montaigne, 75008 Paris, France',
      category: 'hotel',
      coordinates: { lat: 48.8653, lng: 2.2989 },
      business_hours: ['24/7'],
      rating: 4.9,
      price_level: 5,
      photos: ['https://i.pinimg.com/736x/2e/bb/6a/2ebb6a37b9df5ba301284bd7d6dfd59a.jpg'],
      description: 'Luxury hotel with elegant rooms and suites',
      tags: ['luxury', 'hotel', 'accommodation'],
      created_at: '2023-01-01T00:00:00Z'
    },
    // Adding a restaurant
    {
      id: '4',
      name: 'Le Comptoir du Relais',
      address: '9 Carrefour de l\'Odéon, 75006 Paris, France',
      category: 'restaurant',
      coordinates: { lat: 48.8507, lng: 2.3354 },
      business_hours: ['12:00-23:00'],
      rating: 4.5,
      price_level: 3,
      photos: ['https://i.pinimg.com/236x/62/05/cd/6205cd096497ecec2be01679642ddacc.jpg'],
      description: 'Classic French bistro with cozy atmosphere',
      tags: ['bistro', 'french cuisine', 'dining'],
      created_at: '2023-01-01T00:00:00Z'
    }
  ];

export default function ItineraryPage({ params }: { params: { id: string } }) {
    const [locations, setLocations] = React.useState<Location[]>([]);
    const [mapInstance, setMapInstance] = React.useState<google.maps.Map | null>(null);
    const [openDialog, setOpenDialog] = React.useState(false);
    const [pendingLocations, setPendingLocations] = React.useState<Location[]>([]);
    const [selectedLocations, setSelectedLocations] = React.useState<Location[]>([]);

    // Fetch locations data based on destination ID
//   React.useEffect(() => {
//     // Add API call to fetch locations for this destination
//   }, [params.id]);

    React.useEffect(() => {
        setLocations(dummyLocations);
    }, []);

    const handleMapLoad = useCallback((map: google.maps.Map) => {
        setMapInstance(map);
    }, []);

    const handleLocationClick = useCallback((location: Location) => {
        if (!mapInstance) return;

        mapInstance.panTo({ lat: location.coordinates.lat, lng: location.coordinates.lng });
        mapInstance.setZoom(18);
    }, [mapInstance]);
    
    const handleLocationsUpdate = (newLocations: Location[]) => {
        setPendingLocations(newLocations);
        setOpenDialog(true);
    };
    
    // Add dialog confirmation handler
    const handleConfirmAdd = () => {
        setLocations(prev => [...prev, ...pendingLocations]);
        setPendingLocations([]);
        setOpenDialog(false);
    };
    
    // Add dialog cancel handler
    const handleCancelAdd = () => {
        setPendingLocations([]);
        setOpenDialog(false);
    };

    return (
        <Container>
            <Box sx={{ my: 4 }}>
                <Typography variant="h4" gutterBottom>
                    Plan Your Trip
                </Typography>
                <TravelInfoExtrationURLInput 
                    onLocationsUpdate={handleLocationsUpdate}
                />
                <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                    <Box sx={{ width: '40%' }}>
                        <Itinerary 
                            locations={locations} 
                            onLocationClick={handleLocationClick}
                        />
                    </Box>
                    <Box sx={{ width: '60%' }}>
                        <MapComponent 
                            locations={locations} 
                            onMapLoad={handleMapLoad}
                        />
                    </Box>
                </Box>
            </Box>

            <Dialog 
                open={openDialog}
                onClose={handleCancelAdd}
                fullWidth
                maxWidth="sm"
                >
                <DialogTitle>Confirm New Locations</DialogTitle>
                <DialogContent>
                    <FormGroup>
                        {pendingLocations.map((location, index) => (
                            <Box key={location.id} sx={{ mb: 2 }}>
                                <FormControlLabel 
                                    control={
                                        <Checkbox 
                                            checked={selectedLocations.some(loc => loc.id === location.id)}
                                            onChange={(event) => {
                                                if (event.target.checked) {
                                                    setSelectedLocations(prev => [...prev, location]);
                                                } else {
                                                    setSelectedLocations(prev => prev.filter(loc => loc.id !== location.id));
                                                }
                                            }}
                                        />
                                    } 
                                    label={
                                        <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                                            <Typography variant="h6">{location.name}</Typography>
                                            {location.photos && location.photos.length > 0 && (
                                                <img src={location.photos[0]} alt={location.name} style={{ width: '50%', height: 'auto', borderRadius: '8px' }} />
                                            )}
                                            <Typography variant="body2" color="text.secondary">{location.address}</Typography>
                                            <Typography variant="body2" color="text.secondary">{location.description}</Typography>
                                            <Typography variant="body2" color="text.secondary">Rating: {location.rating}</Typography>
                                        </Box>
                                    }
                                />
                                {index < pendingLocations.length - 1 && (
                                    <Divider sx={{ mt: 2, mb: 2 }} />
                                )}
                            </Box>
                        ))}
                    </FormGroup>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCancelAdd}>Cancel</Button>
                    <Button 
                        onClick={() => {
                            setLocations(prev => [...prev, ...selectedLocations]);
                            setSelectedLocations([]);
                            setPendingLocations([]);
                            setOpenDialog(false);
                        }}
                        variant="contained" 
                        color="primary"
                    >
                        Add Selected Locations ({selectedLocations.length})
                    </Button>
                </DialogActions>
            </Dialog>
        </Container>
    );
}
