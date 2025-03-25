import React from 'react';
import { Box, Card, CardContent, Typography } from '@mui/material';
import { Location } from '../../types/location';

interface ItineraryProps {
  locations: Location[];
}

export default function Itinerary({ locations }: ItineraryProps) {
  return (
    <Box sx={{ width: '40%', overflowY: 'auto', maxHeight: '400px' }}>
      {locations.map((location) => (
        <Card key={location.id} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h6">{location.name}</Typography>
            <Typography color="textSecondary">{location.address}</Typography>
            {location.description && (
              <Typography variant="body2">{location.description}</Typography>
            )}
          </CardContent>
        </Card>
      ))}
    </Box>
  );
}
