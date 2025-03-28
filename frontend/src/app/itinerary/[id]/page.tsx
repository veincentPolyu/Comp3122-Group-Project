'use client';

import React, { useCallback } from 'react';
import { Box, Button, Container, Dialog, DialogActions, DialogContent, DialogTitle, List, ListItem, ListItemText, Typography } from '@mui/material';
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
        photos: ['eiffel-tower.jpg'],
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
        description: 'World\'s largest art museum and historic monument',
        tags: ['art', 'history', 'museum'],
        created_at: '2023-01-01T00:00:00Z'
    }
];

export default function ItineraryPage({ params }: { params: { id: string } }) {
    const [locations, setLocations] = React.useState<Location[]>([]);
    const [mapInstance, setMapInstance] = React.useState<google.maps.Map | null>(null);
    const [openDialog, setOpenDialog] = React.useState(false);
    const [pendingLocations, setPendingLocations] = React.useState<Location[]>([]);

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
                    <List dense>
                    {pendingLocations.map((location) => (
                        <ListItem key={location.id}>
                        <ListItemText
                            primary={location.name}
                            secondary={location.address}
                        />
                        </ListItem>
                    ))}
                    </List>
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleCancelAdd}>Cancel</Button>
                    <Button 
                    onClick={handleConfirmAdd}
                    variant="contained" 
                    color="primary"
                    >
                    Add Locations ({pendingLocations.length})
                    </Button>
                </DialogActions>
                </Dialog>
        </Container>
    );
}
