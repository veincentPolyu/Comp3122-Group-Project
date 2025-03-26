import React from 'react';
import { 
    Box, Typography, List, ListItem, ListItemIcon, ListItemText,
    Grid, Drawer, Paper, Divider
} from '@mui/material';
import PlaceIcon from '@mui/icons-material/Place';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import HotelIcon from '@mui/icons-material/Hotel';
import { Location } from '../types/location';

const DRAWER_WIDTH = 340;

const NAVIGATION = [
  {
    kind: 'header',
    title: 'Trip Details',
  },
  {
    title: 'Attractions',
    icon: <PlaceIcon />,
    children: [],
  },
  {
    kind: 'divider',
  },
  {
    kind: 'header',
    title: 'Services',
  },
  {
    title: 'Restaurants',
    icon: <RestaurantIcon />,
    children: [],
  },
  {
    title: 'Hotels',
    icon: <HotelIcon />,
    children: [],
  }
];

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
                {location.business_hours && (
                    <Grid item xs={12}>
                        <Typography variant="body2" color="text.secondary">
                            Opening Hours: {location.business_hours.join(', ')}
                        </Typography>
                    </Grid>
                )}
                {location.busy_periods && (
                    <Grid item xs={12}>
                        <Typography variant="body2" color="text.secondary">
                            Busy Periods: {location.busy_periods.join(', ')}
                        </Typography>
                    </Grid>
                )}
                {location.rating && (
                    <Grid item xs={12}>
                        <Typography variant="body2" color="text.secondary">
                            Rating: {location.rating}
                        </Typography>
                    </Grid>
                )}
                {location.price_level && (
                    <Grid item xs={12}>
                        <Typography variant="body2" color="text.secondary">
                            Price Level: {'$'.repeat(location.price_level)}
                        </Typography>
                    </Grid>
                )}
                {location.tags && (
                    <Grid item xs={12}>
                        <Typography variant="body2" color="text.secondary">
                            Tags: {location.tags.join(', ')}
                        </Typography>
                    </Grid>
                )}
                {location.category && (
                    <Grid item xs={12}>
                        <Typography variant="body2" color="text.secondary">
                            Category: {location.category}
                        </Typography>
                    </Grid>
                )}
            </Grid>
        </ListItem>
    );
};

// Main Itinerary component
const Itinerary: React.FC<{ locations: Location[] }> = ({ locations }) => {
    const [expandedItem, setExpandedItem] = React.useState<string | null>(null);
    const [open, setOpen] = React.useState(true);

    // Group locations by category
    React.useEffect(() => {
        NAVIGATION.forEach(item => {
            if (item.title === 'Attractions') {
                item.children = locations.filter(loc => loc.category === 'attraction');
            } else if (item.title === 'Restaurants') {
                item.children = locations.filter(loc => loc.category === 'restaurant');
            } else if (item.title === 'Hotels') {
                item.children = locations.filter(loc => loc.category === 'hotel');
            }
        });
    }, [locations]);

    return (
        <Drawer
            variant="permanent"
            sx={{
                width: DRAWER_WIDTH,
                flexShrink: 0,
                '& .MuiDrawer-paper': {
                    width: DRAWER_WIDTH,
                    boxSizing: 'border-box',
                    position: 'relative',
                    height: '100%',
                },
            }}
        >
            <Box sx={{ overflow: 'auto', p: 2 }}>
                {NAVIGATION.map((item, index) => {
                    if (item.kind === 'header') {
                        return (
                            <Typography
                                key={index}
                                variant="overline"
                                sx={{ px: 3, py: 1, display: 'block', color: 'text.secondary' }}
                            >
                                {item.title}
                            </Typography>
                        );
                    }
                    if (item.kind === 'divider') {
                        return <Divider key={index} sx={{ my: 1 }} />;
                    }
                    return (
                        <React.Fragment key={item.title}>
                            <ListItem button onClick={() => setExpandedItem(expandedItem === item.title ? null : item.title)}>
                                <ListItemIcon>{item.icon}</ListItemIcon>
                                <ListItemText primary={item.title} />
                            </ListItem>
                            {item.children && expandedItem === item.title && (
                                <List disablePadding>
                                    {item.children.map((location) => (
                                        <ItineraryItem key={location.id} location={location} />
                                    ))}
                                </List>
                            )}
                        </React.Fragment>
                    );
                })}
            </Box>
        </Drawer>
    );
};

export default Itinerary;
