import { TextField, Button, Box, CircularProgress } from '@mui/material';
import { useState } from 'react';
import { Location } from '../types/location';

const additionalDummyLocations: Location[] = [
  {
    id: '1',
    name: 'Sainte-Chapelle',
    address: '8 Boulevard du Palais, 75001 Paris, France',
    category: 'attraction',
    coordinates: { lat: 48.8553, lng: 2.3454 },
    business_hours: ['09:30-17:00'],
    rating: 4.9,
    price_level: 2,
    photos: ['https://i.pinimg.com/236x/c6/33/4e/c6334eef379fd137b975e1a94b503c9c.jpg'],
    description: 'Gothic chapel known for its stunning stained glass windows',
    tags: ['chapel', 'stained glass', 'historic monument'],
    created_at: '2023-01-01T00:00:00Z'
  },
  {
    id: '2',
    name: 'Angelina',
    address: '226 Rue de Rivoli, 75001 Paris, France',
    category: 'cafe',
    coordinates: { lat: 48.8631, lng: 2.3322 },
    business_hours: ['08:00-19:00'],
    rating: 4.5,
    price_level: 3,
    photos: ['https://i.pinimg.com/236x/5a/79/14/5a79149e4532147be62a68c107e9be6c.jpg'],
    description: 'Famous for its hot chocolate and elegant atmosphere',
    tags: ['cafe', 'hot chocolate', 'luxury'],
    created_at: '2023-01-01T00:00:00Z'
  },
  {
    id: '3',
    name: 'Musée d\'Orsay',
    address: '1 Rue de la Légion d\'Honneur, 75007 Paris, France',
    category: 'museum',
    coordinates: { lat: 48.8633, lng: 2.3253 },
    business_hours: ['09:30-18:00'],
    rating: 4.8,
    price_level: 3,
    photos: ['https://i.pinimg.com/474x/43/0b/f6/430bf69726c7a80ec6436d7690f351e9.jpg'],
    description: 'Museum housing an impressive collection of Impressionist art',
    tags: ['museum', 'impressionism', 'art'],
    created_at: '2023-01-01T00:00:00Z'
  },
  {
    id: '4',
    name: 'Pont Alexandre III',
    address: 'Pont Alexandre III, 75008 Paris, France',
    category: 'attraction',
    coordinates: { lat: 48.8633, lng: 2.3122 },
    business_hours: ['24/7'],
    rating: 4.7,
    price_level: 0,
    photos: ['https://i.pinimg.com/474x/1b/46/1f/1b461f7c923058b7756259c9dc8520b8.jpg'],
    description: 'Ornate bridge with stunning views of the Seine River',
    tags: ['bridge', 'landmark', 'scenic view'],
    created_at: '2023-01-01T00:00:00Z'
  },
  {
    id: '5',
    name: 'Hôtel des Invalides',
    address: '129 Rue de Grenelle, 75007 Paris, France',
    category: 'attraction',
    coordinates: { lat: 48.8553, lng: 2.3122 },
    business_hours: ['10:00-18:00'],
    rating: 4.6,
    price_level: 2,
    photos: ['https://i.pinimg.com/236x/9d/c2/a6/9dc2a675ea9faeb994a9508203b33145.jpg'],
    description: 'Historic complex housing Napoleon\'s tomb',
    tags: ['military history', 'Napoleon', 'historic monument'],
    created_at: '2023-01-01T00:00:00Z'
  },
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
