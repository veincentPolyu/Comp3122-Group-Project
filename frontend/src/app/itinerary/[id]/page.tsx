'use client';

import React, { useCallback } from 'react';
import { Box, Button, Checkbox, Container, Dialog, DialogActions, DialogContent, DialogTitle, Divider, FormControlLabel, FormGroup, List, ListItem, ListItemText, Typography } from '@mui/material';
import Itinerary from '../../../components/Itinerary';
import { Location } from '../../../types/location';
import TravelInfoExtrationURLInput from '../../../components/TravelInfoExtrationURLInput';
import MapComponent from "../../../components/Map";
import { LocationReview, SuggestedURL } from '../../../types/suggestedURL';

  // suggestedURLs is a list of suggested URLs that the system has chosen for the user based on the user's travel information
  const dummySuggestedURLs: SuggestedURL[] = [
    {
      "creator": 1,
      "url": "https://www.youtube.com/watch?v=IYhMDJvVIF0",
      "tags": [
        "food vlog",
        "Tokyo travel",
        "sushi",
        "omakase",
        "wagyu",
        "ramen"
      ],
      "rate": 4.5,
      "locationsId": [1, 2, 3, 4, 5, 6]
    }
  ];

  // locationReviews is a list of reviews for a location(based on the id) in the itinerary
  const dummyLocationReviews: LocationReview[] = [
    {
      "locationId": 1,
      "creator": 1,
      "url": "https://www.youtube.com/watch?v=IYhMDJvVIF0",
      "review": "A must-visit in Tokyo! Sensoji Temple is steeped in history and offers a serene escape from the city's bustle. The Nakamise shopping street leading up to it is filled with traditional snacks and souvenirs. Highly recommend visiting at night for a magical atmosphere.",
      "rate": 5,
      "updatedAt": "2025-04-05T18:55:00Z"
    },
    {
      "locationId": 2,
      "creator": 1,
      "url": "https://www.youtube.com/watch?v=IYhMDJvVIF0",
      "review": "This Ginza omakase spot is a steal! For only 8200 yen, you get 12 courses of incredible sushi. The chef's skill is top-notch, and the ingredients are so fresh. The sea urchin and fatty tuna were highlights. Definitely worth a visit if you're in Ginza!",
      "rate": 5,
      "updatedAt": "2025-04-05T18:55:00Z"
    },
    {
      "locationId": 3,
      "creator": 1,
      "url": "https://www.youtube.com/watch?v=IYhMDJvVIF0",
      "review": "If you're craving sukiyaki in Shinjuku, this place is a must! All-you-can-eat A5 wagyu for 6000 yen? Yes, please! The beef is gorgeous, and the service is fantastic. Don't forget to dip the beef in the raw egg yolk – it takes it to another level! So satisfying and filling. Highly recommend for a comfy and affordable wagyu feast.",
      "rate": 5,
      "updatedAt": "2025-04-05T18:55:00Z"
    },
    {
      "locationId": 4,
      "creator": 1,
      "url": "https://www.youtube.com/watch?v=IYhMDJvVIF0",
      "review": "Hands down the best tsukemen I've ever had! The mentaiko broth is incredibly rich and flavorful. Be prepared for a short wait, but it's well worth it. Perfect for a cold day in Tokyo.",
      "rate": 5,
      "updatedAt": "2025-04-05T18:55:00Z"
    },
    {
      "locationId": 5,
      "creator": 1,
      "url": "https://www.youtube.com/watch?v=IYhMDJvVIF0",
      "review": "A hidden gem in Hakuba! Their tantan-men is spicy and satisfying, perfect after a day on the slopes. The atmosphere is cozy, and the staff is friendly. Highly recommend for a casual, delicious meal.",
      "rate": 5,
      "updatedAt": "2025-04-05T18:55:00Z"
    },
    {
      "locationId": 6,
      "creator": 1,
      "url": "https://www.youtube.com/watch?v=IYhMDJvVIF0",
      "review": "I had high hopes for Ningyocho Imahan, but it was a bit of a letdown. It's definitely a touristy spot, and for 1000 HKD per person, I expected more. The service felt rushed, and it didn't quite live up to the hype. There are better sukiyaki experiences to be had in Tokyo.",
      "rate": 3,
      "updatedAt": "2025-04-05T18:55:00Z"
    },
    {
        "locationId": 1,
        "creator": 2,
        "url": "https://www.youtube.com/watch?v=hnoDYUdQeyY",
        "review": "Senso-ji Temple is a must-visit for its rich history and vibrant atmosphere. Walking through Nakamise-dori is a sensory delight, with traditional snacks and souvenirs galore. The temple itself is breathtaking, especially during sunset when the crowds dissipate. Don't miss the opportunity to draw omikuji for a fun cultural experience!",
        "rate": 5,
        "updatedAt": "2025-04-05T18:55:00Z"
    },
    {
      "locationId": 7,
      "creator": 2,
      "url": "https://www.youtube.com/watch?v=hnoDYUdQeyY",
      "review": "Asakusa Culture Tourist Information Center is a must-visit for its cleanest restroom and stunning views of Tokyo Skytree from the top. Don't miss the opportunity to grab maps and brochures here!",
      "rate": 5,
      "updatedAt": "2025-04-05T18:55:00Z"
    },
  ];
  
  // detailed info of a location
  const dummyLocations: Location[] = [
    {
      "id": "1",
      "name": "Sensoji Temple",
      "address": "2-3-1 Asakusa, Taito-ku, Tokyo",
      "category": "attraction",
      "coordinates": { "lat": 35.7104, "lng": 139.7967 },
      "business_hours": ["06:00-17:00"],
      "price_level": 1,
      "photos": ["https://i.pinimg.com/236x/b2/26/42/b226428470ffb90dbddf18e9651ba125.jpg"],
      "description": "Tokyo's oldest and most popular temple",
      "tags": ["temple", "historic site"],
      "reviews": [dummyLocationReviews[6], dummyLocationReviews[0]],
      "created_at": "2023-01-01T00:00:00Z"
    },
    {
      "id": "2",
      "name": "Shutoku Sango Ten",
      "address": "Ginza, Chuo-ku, Tokyo",
      "category": "restaurant",
      "coordinates": { "lat": 35.6713, "lng": 139.7659 },
      "business_hours": ["11:00-23:00"],
      "price_level": 3,
      "photos": ["https://tblg.k-img.com/resize/660x370c/restaurant/images/Rvw/136928/136928926.jpg?token=a2bf4fd&api=v2"],
      "description": "12-course omakase with premium ingredients at 8200円",
      "tags": ["sushi", "omakase", "value-for-money"],
      "reviews": [dummyLocationReviews[1]],
      "created_at": "2023-01-01T00:00:00Z"
    },
    {
      "id": "3",
      "name": "Momo Paradise",
      "address": "Kabukicho, Shinjuku, Tokyo",
      "category": "restaurant",
      "coordinates": { "lat": 35.6955, "lng": 139.7026 },
      "business_hours": ["17:00-23:00"],
      "price_level": 2,
      "photos": ["https://tblg.k-img.com/restaurant/images/Rvw/217460/150x150_square_6f3e69d6f99a199f45811a8f126ffd17.jpg"],
      "description": "A5 wagyu all-you-can-eat sukiyaki for 6000円",
      "tags": ["wagyu", "sukiyaki", "all-you-can-eat"],
      "reviews": [dummyLocationReviews[2]],
      "created_at": "2023-01-01T00:00:00Z"
    },
    {
      "id": "4",
      "name": "Ikebukuro Tsukemen King",
      "address": "Ikebukuro, Toshima-ku, Tokyo",
      "category": "restaurant",
      "coordinates": { "lat": 35.7295, "lng": 139.7109 },
      "business_hours": ["11:00-22:00"],
      "price_level": 2,
      "photos": ["https://images.unsplash.com/photo-1569718212165-3a8278d5f624?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80"],
      "description": "Legendary mentaiko tsukemen with rich fish broth",
      "tags": ["ramen", "tsukemen", "local-favorite"],
      "reviews": [dummyLocationReviews[3]],
      "created_at": "2023-01-01T00:00:00Z"
    },
    {
      "id": "6",
      "name": "Ningyocho Imahan",
      "address": "Ueno, Taito-ku, Tokyo",
      "category": "restaurant",
      "coordinates": { "lat": 35.7075, "lng": 139.7744 },
      "business_hours": ["11:00-22:00"],
      "price_level": 4,
      "photos": ["https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2340&q=80"],
      "description": "Historic sukiyaki restaurant with premium wagyu",
      "tags": ["sukiyaki", "wagyu", "tourist-spot"],
      "reviews": [dummyLocationReviews[5]],
      "created_at": "2023-01-01T00:00:00Z"
    },
    {
      "id": "7",
      "name": "Asakusa Culture Tourist Information Center",
      "address": "2-18-9 Kaminarimon, Taito-ku, Tokyo",
      "category": "attraction",
      "coordinates": { "lat": 35.710455, "lng": 139.797249 },
      "business_hours": ["09:00-20:00"],
      "price_level": 0,
      "photos": ["https://i.pinimg.com/236x/72/5d/02/725d0286218a77d5795c9617e348055d.jpg"],
      "description": "Provides maps, brochures, and a great view of Tokyo Skytree from its observation deck.",
      "tags": ["information center", "viewpoint"],
      "reviews": [dummyLocationReviews[7]],
      "created_at": "2023-01-01T00:00:00Z"
    },
  ];
  
  // Suggested locations near Sensoji Temple
  const dummySuggestedLocations: Location[] = [
    {
      id: "s1",
      name: "Toraya Asakusa",
      address: "2-2-2 Asakusa, Taito-ku, Tokyo",
      category: "restaurant",
      coordinates: { lat: 35.7115, lng: 139.7968 },
      business_hours: ["9:00-18:00"],
      price_level: 2,
      photos: ["https://tblg.k-img.com/restaurant/images/Rvw/247447/640x640_rect_ef679ea25057ac51973547ec509c7233.jpg"],
      description: "Traditional Japanese sweets and desserts, perfect for a sweet treat after visiting Sensoji Temple",
      tags: ["dessert", "traditional", "japanese-sweets"],
      reviews: [],
      created_at: "2023-01-01T00:00:00Z"
    },
    {
      id: "s2",
      name: "Kagetsudou",
      address: "Nishiasakusa, Taito-ku, Tokyo",
      category: "bakery",
      coordinates: { lat: 35.7128, lng: 139.8004 },
      business_hours: ["9:00-18:00"],
      price_level: 1,
      photos: ["https://tblg.k-img.com/restaurant/images/Rvw/238791/640x640_rect_d9fc47ebe3a13d67480f790a1a6c54bc.jpg"],
      description: "Famous for its delicious melon pan, a must-try when exploring Asakusa",
      tags: ["bakery", "melon-pan", "snack"],
      reviews: [],
      created_at: "2023-01-01T00:00:00Z"
    },
    {
      id: "s3",
      name: "Kamejuu",
      address: "2-1-1 Kaminarimon, Taito-ku, Tokyo",
      category: "confectionery",
      coordinates: { lat: 35.7113, lng: 139.7975 },
      business_hours: ["9:00-18:00"],
      price_level: 1,
      photos: ["https://tblg.k-img.com/restaurant/images/Rvw/252409/640x640_rect_718b33187b86ffe95fd06b505162a432.jpg"],
      description: "Popular for its traditional dorayaki, a favorite snack of Doraemon",
      tags: ["confectionery", "dorayaki", "traditional"],
      reviews: [],
      created_at: "2023-01-01T00:00:00Z"
    }
  ];
  
  
export default function ItineraryPage({ params }: { params: { id: string } }) {
    const [locations, setLocations] = React.useState<Location[]>([]);
    const [suggestedLocations, setSuggestedLocations] = React.useState<Location[]>([]);
    const [mapInstance, setMapInstance] = React.useState<google.maps.Map | null>(null);
    const [openDialog, setOpenDialog] = React.useState(false);
    const [pendingLocations, setPendingLocations] = React.useState<Location[]>([]);
    const [selectedLocations, setSelectedLocations] = React.useState<Location[]>([]);

    React.useEffect(() => {
        setLocations(dummyLocations);
        // Use the predefined suggestedLocations array
        setSuggestedLocations(dummySuggestedLocations);
    }, []);

    const handleMapLoad = useCallback((map: google.maps.Map) => {
        setMapInstance(map);
    }, []);

    const handleLocationClick = useCallback((location: Location) => {
        if (!mapInstance) return;

        // Pan to the clicked location
        mapInstance.panTo({ lat: location.coordinates.lat, lng: location.coordinates.lng });
        mapInstance.setZoom(18);

        // Show suggested locations on the map
        if (mapInstance) {
            // Clear any existing suggested markers and create new ones
            const event = new CustomEvent('showSuggestedLocations', { detail: location });
            window.dispatchEvent(event);

            const bounds = new google.maps.LatLngBounds();
            
            // Add the clicked location to bounds
            bounds.extend({ lat: location.coordinates.lat, lng: location.coordinates.lng });
            
            // Add suggested locations to bounds
            suggestedLocations.forEach(loc => {
                bounds.extend({ lat: loc.coordinates.lat, lng: loc.coordinates.lng });
            });

            // Fit the map to show both the clicked location and suggested locations
            mapInstance.fitBounds(bounds);
        }
    }, [mapInstance, suggestedLocations]);
    
    const handleLocationRemove = useCallback((locationId: string) => {
        setLocations(prev => prev.filter(loc => loc.id !== locationId));
    }, []);

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
                            suggestedLocations={suggestedLocations}
                            onLocationClick={handleLocationClick}
                            onLocationRemove={handleLocationRemove}
                        />
                    </Box>
                    <Box sx={{ width: '60%', height: '700px' }}>
                        <MapComponent 
                            locations={locations}
                            suggestedLocations={suggestedLocations}
                            onMapLoad={handleMapLoad}
                            onShowSuggestedLocations={(location) => {
                                handleLocationClick(location);
                            }}
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
