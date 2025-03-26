'use client';

import React from 'react';
import { Box, Container, Typography } from '@mui/material';
import Map from '../../../components/Map';
import Itinerary from '../../../components/Itinerary';
import { Location } from '../../../types/location';

const dummyLocations: Location[] = [
    {
        id: '1',
        name: 'Eiffel Tower',
        address: 'Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France',
        category: 'attraction',
        coordinates: { lat: 48.8584, lng: 2.2945 },
        business_hours: ['09:00-00:00', '09:00-00:00', '09:00-00:00', '09:00-00:00', '09:00-00:00', '09:00-00:00', '09:00-00:00'],
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
        business_hours: ['09:00-18:00', '09:00-18:00', 'closed', '09:00-18:00', '09:00-18:00', '09:00-18:00', '09:00-18:00'],
        rating: 4.8,
        price_level: 3,
        description: 'World\'s largest art museum and historic monument',
        tags: ['art', 'history', 'museum'],
        created_at: '2023-01-01T00:00:00Z'
    }
];

export default function ItineraryPage({ params }: { params: { id: string } }) {
    const [locations, setLocations] = React.useState<Location[]>([]);

    // Fetch locations data based on destination ID
//   React.useEffect(() => {
//     // Add API call to fetch locations for this destination
//   }, [params.id]);

    React.useEffect(() => {
        setLocations(dummyLocations);
    }, []);
    
    return (
        <Container>
            <Box sx={{ my: 4 }}>
                <Typography variant="h4" gutterBottom>
                    Plan Your Trip
                </Typography>
                <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                    <Box sx={{ width: '40%' }}>
                        <Itinerary locations={locations} />
                    </Box>
                    <Box sx={{ width: '60%' }}>
                        <Map locations={locations} />
                    </Box>
                </Box>
            </Box>
        </Container>
    );
}
