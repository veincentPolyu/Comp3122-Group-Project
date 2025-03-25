'use client';

import { Box, Container } from '@mui/material';
import { useState } from 'react';
import UrlInput from '../components/UrlInput';
import Map from '../components/Map';
import Itinerary from '../components/Itinerary';
import { Location } from '../types/location';
import Hero from '../components/Hero';
import React from 'react';

export default function Home() {
  const [locations, setLocations] = useState<Location[]>([]);

  return (
    <>
      <Container>
        {/* <Hero/> */}
        <Box sx={{ my: 4 }}>
          {/* <UrlInput onLocationsUpdate={setLocations} />
          <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
            <Map locations={locations} />
            <Itinerary locations={locations} />
          </Box> */}
        </Box>
      </Container>
    </>
  );
}
