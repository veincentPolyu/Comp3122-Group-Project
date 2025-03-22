import { GoogleMap, useLoadScript, Marker } from '@react-google-maps/api';
import { Box, CircularProgress } from '@mui/material';
import { useMemo } from 'react';
import { Location } from '../services/api';

interface MapProps {
  locations?: Location[];
}

const Map = ({ locations = [] }: MapProps) => {
  const { isLoaded } = useLoadScript({
    googleMapsApiKey: process.env.REACT_APP_GOOGLE_MAPS_API_KEY || '',
  });

  const center = useMemo(() => ({ lat: 0, lng: 0 }), []);

  if (!isLoaded) return <CircularProgress />;

  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <GoogleMap zoom={2} center={center} mapContainerClassName="map-container">
        {locations.map((location) => (
          <Marker
            key={location.id}
            position={location.coordinates}
            title={location.name}
          />
        ))}
      </GoogleMap>
    </Box>
  );
};

export default Map;
