import React from 'react';
import { 
    Box, Typography, List, ListItem, ListItemIcon, ListItemText,
    Grid, Drawer, Paper, Divider,
    Card, CardContent, IconButton, Rating,
    Chip, Stack, Collapse, Button, Link,
    Avatar, Tooltip
} from '@mui/material';
import PlaceIcon from '@mui/icons-material/Place';
import RestaurantIcon from '@mui/icons-material/Restaurant';
import HotelIcon from '@mui/icons-material/Hotel';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ExpandLessIcon from '@mui/icons-material/ExpandLess';
import AccessTimeIcon from '@mui/icons-material/AccessTime';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import StarIcon from '@mui/icons-material/Star';
import ReviewsIcon from '@mui/icons-material/Reviews';
import Slider from 'react-slick';
import { Location } from '../types/location';
import DeleteIcon from '@mui/icons-material/Delete';
import ThumbUpIcon from '@mui/icons-material/ThumbUp';
import ThumbDownIcon from '@mui/icons-material/ThumbDown';
import VideoLibraryIcon from '@mui/icons-material/VideoLibrary';

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
    suggestedLocations?: Location[];
    onLocationClick?: (location: Location) => void;
    onLocationRemove?: (locationId: string) => void;
}

// ItineraryItem component
const ItineraryItem: React.FC<{ 
    location: Location;
    onClick?: (location: Location) => void;
    onRemove?: (locationId: string) => void;
    onShowRecommended?: (location: Location) => void;
    isFirst?: boolean;
}> = ({ location, onClick, onRemove, onShowRecommended, isFirst }) => {
    const [showReviews, setShowReviews] = React.useState(false);
    const [reviewVotes, setReviewVotes] = React.useState<Record<number, 'up' | 'down' | null>>({});

    const handleLocationClick = (event: React.MouseEvent) => {
        if (!event.target || !(event.target as HTMLElement).closest('.reviews-section, .remove-button')) {
            onClick?.(location);
        }
    };

    const handleVote = (reviewId: number, voteType: 'up' | 'down') => {
        setReviewVotes(prev => ({
            ...prev,
            [reviewId]: prev[reviewId] === voteType ? null : voteType
        }));
    };

    return (
        <Box sx={{ py: 2 }}>
            <Card 
                sx={{ 
                    '&:hover': {
                        boxShadow: 6
                    },
                    width: '100%',
                    minWidth: 280,
                    maxWidth: '100%',
                    overflow: 'visible'
                }}
            >
                <CardContent sx={{ p: 2, '&:last-child': { pb: 2 } }}>
                    {/* Location Section - Clickable */}
                    <Box 
                        onClick={handleLocationClick}
                        sx={{ 
                            cursor: 'pointer',
                            '&:hover': {
                                bgcolor: 'action.hover'
                            },
                            position: 'relative'
                        }}
                    >
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                            <Typography 
                                variant="h6" 
                                sx={{ 
                                    pr: 4,
                                    wordBreak: 'break-word'
                                }}
                            >
                                {location.name}
                            </Typography>
                            <Box className="remove-button" sx={{ flexShrink: 0 }}>
                                <IconButton 
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        onRemove?.(location.id);
                                    }}
                                    color="error"
                                    size="small"
                                >
                                    <DeleteIcon />
                                </IconButton>
                            </Box>
                        </Box>

                        {location.photos && location.photos.length > 0 && (
                            <Box sx={{ 
                                position: 'relative', 
                                borderRadius: '8px', 
                                overflow: 'hidden',
                                mb: 2,
                                width: '100%'
                            }}>
                                <img 
                                    src={location.photos[0]} 
                                    alt={location.name} 
                                    style={{ 
                                        width: '100%', 
                                        height: '200px', 
                                        objectFit: 'cover',
                                        borderRadius: '8px'
                                    }} 
                                />
                            </Box>
                        )}

                        <Stack spacing={1.5}>
                            <Typography variant="body2" color="text.secondary" sx={{ 
                                display: 'flex', 
                                alignItems: 'center', 
                                gap: 1,
                                wordBreak: 'break-word'
                            }}>
                                <PlaceIcon fontSize="small" />
                                {location.address}
                            </Typography>

                            {location.business_hours && (
                                <Typography variant="body2" color="text.secondary" sx={{ 
                                    display: 'flex', 
                                    alignItems: 'center', 
                                    gap: 1 
                                }}>
                                    <AccessTimeIcon fontSize="small" />
                                    {location.business_hours.join(', ')}
                                </Typography>
                            )}

                            {location.rating && (
                                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                                    <Rating 
                                        value={location.rating} 
                                        readOnly 
                                        precision={0.5}
                                        size="small"
                                    />
                                    <Typography variant="body2" color="text.secondary">
                                        {location.rating}
                                    </Typography>
                                </Box>
                            )}

                            {location.price_level && (
                                <Typography variant="body2" color="text.secondary" sx={{ 
                                    display: 'flex', 
                                    alignItems: 'center', 
                                    gap: 1 
                                }}>
                                    <AttachMoneyIcon fontSize="small" />
                                    {'$'.repeat(location.price_level)}
                                </Typography>
                            )}

                            {location.description && (
                                <Typography variant="body2" sx={{ wordBreak: 'break-word' }}>
                                    {location.description}
                                </Typography>
                            )}

                            {location.tags && location.tags.length > 0 && (
                                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                                    {location.tags.map((tag, index) => (
                                        <Chip 
                                            key={index} 
                                            label={tag} 
                                            size="small" 
                                            variant="outlined"
                                            sx={{ borderRadius: 1 }}
                                        />
                                    ))}
                                </Box>
                            )}

                            <Stack spacing={1} sx={{ mt: 2 }}>
                                <Button
                                    variant="outlined"
                                    size="small"
                                    startIcon={<PlaceIcon />}
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        // TODO: Implement find related spots functionality
                                    }}
                                >
                                    Find similar Spots
                                </Button>
                                <Button
                                    variant="outlined"
                                    size="small"
                                    startIcon={<StarIcon />}
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        onShowRecommended?.(location);
                                    }}
                                >
                                    Recommended Spots Nearby
                                </Button>
                            </Stack>
                        </Stack>
                    </Box>

                    {/* Reviews Section - Not Clickable */}
                    <Box className="reviews-section" sx={{ mt: 2 }}>
                        <Divider sx={{ my: 2 }} />
                        <Box 
                            onClick={() => setShowReviews(!showReviews)}
                            sx={{ 
                                display: 'flex', 
                                alignItems: 'center', 
                                justifyContent: 'space-between',
                                cursor: 'pointer',
                                '&:hover': { bgcolor: 'action.hover' },
                                p: 1,
                                borderRadius: 1
                            }}
                        >
                            <Typography 
                                variant="subtitle1" 
                                sx={{ 
                                    display: 'flex', 
                                    alignItems: 'center', 
                                    gap: 1 
                                }}
                            >
                                <ReviewsIcon />
                                Reviews ({location.reviews?.length || 0})
                            </Typography>
                            {showReviews ? <ExpandLessIcon /> : <ExpandMoreIcon />}
                        </Box>

                        <Collapse in={showReviews}>
                            <Box sx={{ 
                                maxWidth: '100%', 
                                overflowX: 'hidden',
                                maxHeight: '400px',
                                overflowY: 'auto',
                                '&::-webkit-scrollbar': {
                                    width: '8px',
                                },
                                '&::-webkit-scrollbar-track': {
                                    backgroundColor: 'background.paper',
                                },
                                '&::-webkit-scrollbar-thumb': {
                                    backgroundColor: 'grey.400',
                                    borderRadius: '4px',
                                    '&:hover': {
                                        backgroundColor: 'grey.500',
                                    },
                                },
                            }}>
                                {location.reviews && location.reviews.length > 0 ? (
                                    <List sx={{ width: '100%', p: 0 }}>
                                        {location.reviews.map((review, index) => (
                                            <React.Fragment key={index}>
                                                <ListItem sx={{ 
                                                    display: 'block', 
                                                    py: 2, 
                                                    px: 0,
                                                    width: '100%'
                                                }}>
                                                    <Box sx={{ 
                                                        display: 'flex', 
                                                        alignItems: 'flex-start', 
                                                        gap: 2,
                                                        width: '100%'
                                                    }}>
                                                        <Avatar sx={{ flexShrink: 0 }}>
                                                            {review.creator.toString()[0]}
                                                        </Avatar>
                                                        <Box sx={{ 
                                                            flex: 1,
                                                            minWidth: 0, // This helps with text overflow
                                                            width: '100%'
                                                        }}>
                                                            <Box sx={{ 
                                                                display: 'flex', 
                                                                alignItems: 'center', 
                                                                gap: 1, 
                                                                mb: 1,
                                                                flexWrap: 'wrap'
                                                            }}>
                                                                <Typography variant="subtitle2" noWrap>
                                                                    Creator #{review.creator}
                                                                </Typography>
                                                                <Typography variant="caption" color="text.secondary">
                                                                    {new Date(review.updatedAt).toLocaleDateString()}
                                                                </Typography>
                                                            </Box>
                                                            <Box sx={{ 
                                                                display: 'flex', 
                                                                alignItems: 'center', 
                                                                gap: 1, 
                                                                mb: 1,
                                                                flexWrap: 'wrap'
                                                            }}>
                                                                <Rating value={review.rate} readOnly size="small" />
                                                                {review.url && (
                                                                    <Tooltip title="View review video/post">
                                                                        <IconButton 
                                                                            size="small" 
                                                                            component={Link} 
                                                                            href={review.url}
                                                                            target="_blank"
                                                                        >
                                                                            <VideoLibraryIcon fontSize="small" />
                                                                        </IconButton>
                                                                    </Tooltip>
                                                                )}
                                                            </Box>
                                                            <Typography 
                                                                variant="body2" 
                                                                sx={{ 
                                                                    mb: 1,
                                                                    wordBreak: 'break-word'
                                                                }}
                                                            >
                                                                {review.review}
                                                            </Typography>
                                                            <Box sx={{ 
                                                                display: 'flex', 
                                                                gap: 1,
                                                                flexWrap: 'wrap'
                                                            }}>
                                                                <Button
                                                                    size="small"
                                                                    startIcon={<ThumbUpIcon />}
                                                                    variant={reviewVotes[review.creator] === 'up' ? 'contained' : 'outlined'}
                                                                    onClick={() => handleVote(review.creator, 'up')}
                                                                >
                                                                    Helpful
                                                                </Button>
                                                                <Button
                                                                    size="small"
                                                                    startIcon={<ThumbDownIcon />}
                                                                    variant={reviewVotes[review.creator] === 'down' ? 'contained' : 'outlined'}
                                                                    onClick={() => handleVote(review.creator, 'down')}
                                                                >
                                                                    Not Helpful
                                                                </Button>
                                                            </Box>
                                                        </Box>
                                                    </Box>
                                                </ListItem>
                                                {index < location.reviews.length - 1 && (
                                                    <Divider component="li" />
                                                )}
                                            </React.Fragment>
                                        ))}
                                    </List>
                                ) : (
                                    <Typography variant="body2" color="text.secondary" sx={{ p: 2 }}>
                                        No reviews available yet.
                                    </Typography>
                                )}
                            </Box>
                        </Collapse>
                    </Box>
                </CardContent>
            </Card>
        </Box>
    );
};

// Custom arrow components
const NextArrow = ({ onClick }: { onClick?: () => void }) => (
    <IconButton
        onClick={onClick}
        sx={{
            position: 'absolute',
            right: -20,
            top: '50%',
            transform: 'translateY(-50%)',
            zIndex: 2,
            bgcolor: 'background.paper',
            boxShadow: 2,
            width: 40,
            height: 40,
            '&:hover': { 
                bgcolor: 'background.paper',
                boxShadow: 3
            }
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
            left: -20,
            top: '50%',
            transform: 'translateY(-50%)',
            zIndex: 2,
            bgcolor: 'background.paper',
            boxShadow: 2,
            width: 40,
            height: 40,
            '&:hover': { 
                bgcolor: 'background.paper',
                boxShadow: 3
            }
        }}
    >
        <NavigateBeforeIcon />
    </IconButton>
);

// Main Itinerary component
const Itinerary: React.FC<ItineraryProps> = ({ 
    locations, 
    suggestedLocations = [], 
    onLocationClick, 
    onLocationRemove 
}) => {
    const [expandedItem, setExpandedItem] = React.useState<string | null>(null);

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
                height: '100%',
                '& .MuiDrawer-paper': {
                    width: DRAWER_WIDTH,
                    boxSizing: 'border-box',
                    position: 'relative',
                    height: '100%',
                    overflowY: 'visible',
                },
            }}
        >
            <Box sx={{ 
                overflow: 'auto', 
                p: 2,
                height: '100%',
                '& .slick-slider': {
                    position: 'relative',
                    '& .slick-list': {
                        overflow: 'visible',
                    },
                    '& .slick-track': {
                        display: 'flex',
                        '& .slick-slide': {
                            height: 'auto',
                            '& > div': {
                                height: '100%',
                            },
                        },
                    },
                },
            }}>
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
                                        {item.children.map((location, idx) => (
                                            <Box key={location.id} sx={{ px: 1 }}>
                                                <ItineraryItem 
                                                    location={location}
                                                    onClick={onLocationClick}
                                                    onRemove={onLocationRemove}
                                                    onShowRecommended={onLocationClick}
                                                    isFirst={idx === 0}
                                                />
                                            </Box>
                                        ))}
                                    </Slider>
                                </Box>
                            )}
                        </React.Fragment>
                    );
                })}

                {suggestedLocations.length > 0 && (
                    <>
                        <Divider sx={{ my: 1 }} />
                        <Typography
                            variant="overline"
                            sx={{ px: 3, py: 1, display: 'block', color: 'text.secondary' }}
                        >
                            Suggestions
                        </Typography>
                        <ListItem button onClick={() => setExpandedItem(expandedItem === 'suggestions' ? null : 'suggestions')}>
                            <ListItemIcon><PlaceIcon /></ListItemIcon>
                            <ListItemText primary="Suggested Places" />
                        </ListItem>
                        {expandedItem === 'suggestions' && (
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
                                    {suggestedLocations.map((location, idx) => (
                                        <Box key={location.id} sx={{ px: 1 }}>
                                            <ItineraryItem 
                                                location={location}
                                                onClick={onLocationClick}
                                                onRemove={onLocationRemove}
                                                onShowRecommended={onLocationClick}
                                                isFirst={idx === 0}
                                            />
                                        </Box>
                                    ))}
                                    
                                </Slider>
                            </Box>
                        )}
                    </>
                )}
            </Box>
        </Drawer>
    );
};

export default Itinerary;
