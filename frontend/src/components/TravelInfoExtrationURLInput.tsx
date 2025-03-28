import { TextField, Button, Box, CircularProgress } from '@mui/material';
import { useState } from 'react';
import { Location } from '../types/location';

const additionalDummyLocations: Location[] = [
    {
        id: '3',
        name: 'Arc de Triomphe',
        address: 'Place Charles de Gaulle, 75008 Paris, France',
        category: 'attraction',
        coordinates: { lat: 48.8739, lng: 2.2950 },
        business_hours: ['10:00-22:30'],
        rating: 4.6,
        price_level: 2,
        description: 'Triumphal arch honoring the soldiers who fought and died for France',
        tags: ['landmark', 'monument'],
        created_at: '2023-01-01T00:00:00Z'
    },
// Add more locations here...
];

interface UrlInputProps {
  onLocationsUpdate: (locations: any[]) => void;
}

const TravelInfoExtrationURLInput = ({ onLocationsUpdate }: UrlInputProps) => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      // const result = await processUrl(url);
      //onLocationsUpdate(result.locations);
      onLocationsUpdate(additionalDummyLocations);
    } catch (error) {
      console.error('Error processing URL:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ display: 'flex', gap: 2 }}>
      <TextField 
        fullWidth
        label="Enter URL (blog, video, or social media post)"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        disabled={loading}
      />
      <Button 
        variant="contained" 
        onClick={handleSubmit}
        disabled={loading}
        startIcon={loading ? <CircularProgress size={20} /> : null}
      >
        Process
      </Button>
    </Box>
  );
};

export default TravelInfoExtrationURLInput;
