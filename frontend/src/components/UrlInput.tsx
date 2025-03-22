import { TextField, Button, Box, CircularProgress } from '@mui/material';
import { useState } from 'react';
import { processUrl } from '../services/api';

interface UrlInputProps {
  onLocationsUpdate: (locations: any[]) => void;
}

const UrlInput = ({ onLocationsUpdate }: UrlInputProps) => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      const result = await processUrl(url);
      onLocationsUpdate(result.locations);
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

export default UrlInput;
