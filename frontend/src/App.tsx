import { Box, Container, CssBaseline, ThemeProvider } from '@mui/material';
import { useState } from 'react';
import UrlInput from './components/UrlInput';
import Map from './components/Map';
import Itinerary from './components/Itinerary';
import { Location } from './types/location';
import { theme } from './theme';
import React from 'react';

function App() {
  const [locations, setLocations] = useState<Location[]>([]);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container>
        <Box sx={{ my: 4 }}>
          <UrlInput onLocationsUpdate={setLocations} />
          <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
            <Map locations={locations} />
            <Itinerary locations={locations} />
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
