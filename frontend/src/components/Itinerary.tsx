import React from 'react';
import { 
    Box, Typography, List, ListItem, ListItemIcon, ListItemText,
    Grid, Drawer, Paper, Divider,
    Card,
    CardContent,
    IconButton
} from '@mui/material';
import PlaceIcon from '@mui/icons-material/Place';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import HotelIcon from '@mui/icons-material/Hotel';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import Slider from 'react-slick';
import { Location } from '../types/location';

import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

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

interface ItineraryProps {
    locations: Location[];
    onLocationClick?: (location: Location) => void;
}

// ItineraryItem component
const ItineraryItem: React.FC<{ 
    location: Location;
    onClick?: (location: Location) => void;
}> = ({ location, onClick }) => {
    return (
        <Card 
            sx={{ 
                mb: 2,
                cursor: 'pointer',
                '&:hover': {
                    bgcolor: 'action.hover'
                }
            }}
            onClick={() => onClick?.(location)}
        >
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    {location.name}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                    Address: {location.address}
                </Typography>
                {location.description && (
                    <Typography variant="body2" sx={{ mt: 1 }}>
                        {location.description}
                    </Typography>
                )}
                {location.business_hours && (
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Opening Hours: {location.business_hours.join(', ')}
                    </Typography>
                )}
                {location.busy_periods && (
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Busy Periods: {location.busy_periods.join(', ')}
                    </Typography>
                )}
                {location.rating && (
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Rating: {location.rating}
                    </Typography>
                )}
                {location.price_level && (
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Price Level: {'$'.repeat(location.price_level)}
                    </Typography>
                )}
                {location.tags && (
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Tags: {location.tags.join(', ')}
                    </Typography>
                )}
                {location.category && (
                    <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                        Category: {location.category}
                    </Typography>
                )}
            </CardContent>
        </Card>
    );
};

// Custom arrow components
const NextArrow = ({ onClick }: { onClick?: () => void }) => (
  <IconButton
    onClick={onClick}
    sx={{
      position: 'absolute',
      right: -10,
      top: '50%',
      transform: 'translateY(-50%)',
      zIndex: 1,
      bgcolor: 'background.paper',
      boxShadow: 1,
      '&:hover': { bgcolor: 'background.paper' }
    }}
  >
    <NavigateNextIcon />
  </IconButton>
);

const PrevArrow = ({ onClick }: { onClick?: () => void }) => (
  <IconButton
    onClick={onClick}
    sx={{
      position: 'absolute',
      left: -10,
      top: '50%',
      transform: 'translateY(-50%)',
      zIndex: 1,
      bgcolor: 'background.paper',
      boxShadow: 1,
      '&:hover': { bgcolor: 'background.paper' }
    }}
  >
    <NavigateBeforeIcon />
  </IconButton>
);

// Main Itinerary component
const Itinerary: React.FC<ItineraryProps> = ({ locations, onLocationClick }) => {
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
                                <Box sx={{ px: 2, py: 1 }}>
                                    <Slider
                                        dots={false}
                                        infinite={false}
                                        speed={500}
                                        slidesToShow={1}
                                        slidesToScroll={1}
                                        nextArrow={<NextArrow />}
                                        prevArrow={<PrevArrow />}
                                        adaptiveHeight
                                    >
                                        {item.children.map((location) => (
                                            <Box key={location.id} sx={{ px: 1 }}>
                                                <ItineraryItem 
                                                    location={location}
                                                    onClick={onLocationClick}
                                                />
                                            </Box>
                                        ))}
                                    </Slider>
                                </Box>
                            )}
                        </React.Fragment>
                    );
                })}
            </Box>
        </Drawer>
    );
};

export default Itinerary;
