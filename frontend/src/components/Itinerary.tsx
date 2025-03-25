import React from 'react';
import { 
    Box, 
    Typography, 
    Paper, 
    List, 
    ListItem, 
    ListItemText,
    Grid 
} from '@mui/material';
import { Location } from '../services/api';

// ItineraryItem component
const ItineraryItem: React.FC<{ location: Location }> = ({ location }) => {
    return (
        <ListItem component={Paper} elevation={2} sx={{ mb: 2, p: 2 }}>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                    <Typography variant="h6">
                        {location.name}
                    </Typography>
                </Grid>
                <Grid item xs={12}>
                    <Typography variant="body1" color="text.secondary">
                        Address: {location.address}
                    </Typography>
                </Grid>
                {location.description && (
                    <Grid item xs={12}>
                        <Typography variant="body2">
                            {location.description}
                        </Typography>
                    </Grid>
                )}
                {location.businessHours && (
                    <Grid item xs={12}>
                        <Typography variant="body2" color="text.secondary">
                            Opening Hours: {location.businessHours}
                        </Typography>
                    </Grid>
                )}
            </Grid>
        </ListItem>
    );
};

// Main Itinerary component
const Itinerary: React.FC<{ locations: Location[] }> = ({ locations }) => {
    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Itinerary
            </Typography>
            <List>
                {locations.map((location) => (
                    <ItineraryItem
                        key={location.id}
                        location={location}
                    />
                ))}
            </List>
        </Box>
    );
};

export default Itinerary;
