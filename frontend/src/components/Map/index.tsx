import React from 'react';
import { GoogleMap, LoadScript, Marker } from '@react-google-maps/api';
import { Location } from '../../types/location';
import { Box } from '@mui/material';

interface MapProps {
  locations: Location[];
}

const containerStyle = {
  width: '100%',
  height: '400px'
};

const center = {
  lat: 35.6762,
  lng: 139.6503
};

export default function Map({ locations }: MapProps) {
  return (
    <Box sx={{ width: '60%' }}>
      <LoadScript googleMapsApiKey={process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY || ''}>
        <GoogleMap
          mapContainerStyle={containerStyle}
          center={center}
          zoom={11}
        >
          {locations.map((location) => (
            <Marker
              key={location.id}
              position={location.coordinates}
              title={location.name}
            />
          ))}
        </GoogleMap>
      </LoadScript>
    </Box>
  );
}
