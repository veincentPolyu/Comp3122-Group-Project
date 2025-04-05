'use client';

import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import InputLabel from '@mui/material/InputLabel';
import Link from '@mui/material/Link';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import visuallyHidden from '@mui/utils/visuallyHidden';
import { styled } from '@mui/material/styles';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
import Autocomplete from '@mui/material/Autocomplete';
import { useRouter } from 'next/navigation';

const StyledBox = styled('div')(({ theme }) => ({
  alignSelf: 'center',
  width: '100%',
  height: 400,
  marginTop: theme.spacing(8),
  borderRadius: theme.shape.borderRadius,
  outline: '6px solid',
  outlineColor: 'hsla(220, 25%, 80%, 0.2)',
  border: '1px solid',
  borderColor: theme.palette.grey[200],
  boxShadow: '0 0 12px 8px hsla(220, 25%, 80%, 0.2)',
  backgroundImage: 'url(/images/travel-bg.jpg)',
  backgroundSize: 'cover',
  backgroundPosition: 'center',
  [theme.breakpoints.up('sm')]: {
    marginTop: theme.spacing(10),
    height: 700,
  },
  ...(theme.palette.mode === 'dark' && {
    boxShadow: '0 0 24px 12px hsla(210, 100%, 25%, 0.2)',
    outlineColor: 'hsla(220, 20%, 42%, 0.1)',
    borderColor: theme.palette.grey[700],
  }),
}));

const travelTags = [
  { id: 'adventure', label: 'Adventure Travel (hiking, biking, etc.)', checked: false },
  { id: 'cultural', label: 'Cultural Exploration (museums, historical sites)', checked: false },
  { id: 'food', label: 'Food and Wine', checked: false },
  { id: 'wellness', label: 'Relaxation and Wellness', checked: false },
  { id: 'sports', label: 'Sports and Fitness', checked: false },
];

export default function Hero() {
  const [isClient, setIsClient] = React.useState(false);
  const [selectedTags, setSelectedTags] = React.useState<string[]>([]);
  const [location, setLocation] = React.useState<string>('');

  const router = useRouter();
  
  React.useEffect(() => {
    setIsClient(true);
  }, []);

  const handleTagChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const tagId = event.target.name;
    setSelectedTags(prev => 
      event.target.checked 
        ? [...prev, tagId]
        : prev.filter(id => id !== tagId)
    );
  };

  const handleSearch = () => {
    router.push('/itinerary/1');
  };

  if (!isClient) {
    return null;
  }

  return (
    <Box
      id="hero"
      sx={(theme) => ({
        width: '100%',
        backgroundRepeat: 'no-repeat',
        backgroundImage:
          'radial-gradient(ellipse 80% 50% at 50% -20%, hsl(210, 100%, 90%), transparent)',
        ...theme.applyStyles('dark', {
          backgroundImage:
            'radial-gradient(ellipse 80% 50% at 50% -20%, hsl(210, 100%, 16%), transparent)',
        }),
      })}
    >
      <Container
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          pt: { xs: 14, sm: 20 },
          pb: { xs: 8, sm: 12 },
        }}
      >
        <Stack
          spacing={3}
          useFlexGap
          sx={{ 
            alignItems: 'center', 
            width: { xs: '100%', sm: '80%' },
            maxWidth: '800px',
            backgroundColor: 'background.paper',
            p: 4,
            borderRadius: 2,
            boxShadow: 3,
          }}
        >
          <Typography
            variant="h1"
            sx={{
              display: 'flex',
              flexDirection: { xs: 'column', sm: 'row' },
              alignItems: 'center',
              fontSize: 'clamp(2.5rem, 8vw, 3rem)',
              textAlign: 'center',
            }}
          >
            Plan Your Perfect Trip
          </Typography>
          <Typography
            sx={{
              textAlign: 'center',
              color: 'text.secondary',
              width: { sm: '100%', md: '80%' },
              mb: 2,
            }}
          >
            Discover amazing destinations and create unforgettable experiences tailored to your interests
          </Typography>

          <Autocomplete
            fullWidth
            freeSolo
            options={[]}
            value={location}
            onChange={(_, newValue) => setLocation(newValue || '')}
            onInputChange={(_, newValue) => setLocation(newValue)}
            renderInput={(params) => (
              <TextField
                {...params}
                label="Where do you want to go?"
                variant="outlined"
                placeholder="Enter a destination"
                fullWidth
              />
            )}
          />

          <Typography variant="h6" sx={{ alignSelf: 'flex-start', mt: 2 }}>
            What interests you?
          </Typography>
          
          <FormGroup sx={{ width: '100%' }}>
            {travelTags.map((tag) => (
              <FormControlLabel
                key={tag.id}
                control={
                  <Checkbox
                    checked={selectedTags.includes(tag.id)}
                    onChange={handleTagChange}
                    name={tag.id}
                  />
                }
                label={tag.label}
              />
            ))}
          </FormGroup>

          <Button
            variant="contained"
            color="primary"
            size="large"
            fullWidth
            onClick={handleSearch}
            sx={{ mt: 2 }}
          >
            Search
          </Button>
        </Stack>
      </Container>
    </Box>
  );
}