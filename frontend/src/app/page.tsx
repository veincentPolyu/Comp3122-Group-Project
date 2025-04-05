'use client';

import React from 'react';
import { Box, Container, Grid, Card, CardContent, CardMedia, Typography, CardActionArea } from '@mui/material';
import { useRouter } from 'next/navigation';
import Hero from '../components/Hero';

interface DestinationCard {
  id: string;
  title: string;
  description: string;
  imageUrl: string;
}

const destinations: DestinationCard[] = [
  {
    id: '1',
    title: 'Tokyo',
    description: 'Experience the blend of tradition and future in Japan\'s capital',
    imageUrl: 'https://i.pinimg.com/736x/99/a5/f2/99a5f20fdee57e12010f055840eda500.jpg',
  },
  {
    id: '2',
    title: 'Kyoto',
    description: 'Discover ancient temples and beautiful gardens',
    imageUrl: 'https://i.pinimg.com/736x/ee/78/44/ee7844c2fdfaa48dd7ddf978acc5fd30.jpg',
  },
  {
    id: '3',
    title: 'Paris',
    description: 'Explore the city of lights with its iconic landmarks and rich culture',
    imageUrl: 'https://i.pinimg.com/736x/be/08/d9/be08d9d7b0d57f9102f8d6ec3f9e2a0e.jpg',
  },
  // Add more destinations as needed
];

export default function Home() {
  const router = useRouter();

  const handleCardClick = (destinationId: string) => {
    router.push(`/itinerary/${destinationId}`);
  };

  return (
    <>
      <Hero />
      <Container sx={{ py: 8 }}>
        <Typography variant="h4" component="h2" gutterBottom>
          Popular Destinations
        </Typography>
        <Grid container spacing={4}>
          {destinations.map((destination) => (
            <Grid item key={destination.id} xs={12} sm={6} md={4}>
              <Card 
                sx={{ 
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'scale(1.02)',
                  },
                }}
              >
                <CardActionArea onClick={() => handleCardClick(destination.id)}>
                  <CardMedia
                    component="img"
                    height="200"
                    image={destination.imageUrl}
                    alt={destination.title}
                  />
                  <CardContent>
                    <Typography gutterBottom variant="h5" component="h3">
                      {destination.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {destination.description}
                    </Typography>
                  </CardContent>
                </CardActionArea>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </>
  );
}
