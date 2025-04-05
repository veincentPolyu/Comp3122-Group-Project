import { TextField, Button, Box, CircularProgress } from '@mui/material';
import { useState } from 'react';
import { Location } from '../types/location';
import { LocationReview } from '../types/suggestedURL';

const dummyLocationReviews: LocationReview[] = [
  {
    "locationId": 8,
    "creator": 3,
    "url": "https://www.youtube.com/watch?v=E5eGoKd2wQs",
    "review": "Shia Sky is the best observation deck in Tokyo! The views are incredible from every corner, perfect for photos. You can see Shibuya Crossing and even Mt. Fuji if you're lucky. Make a reservation – it's worth it!",
    "rate": 5,
    "updatedAt": "2025-04-05T19:30:00Z"
  },
  {
    "locationId": 9,
    "creator": 3,
    "url": "https://www.youtube.com/watch?v=E5eGoKd2wQs",
    "review": "Shibuya Crossing is a must-see! Over 3,000 people cross during the green light. Check out Shibuya Sky, Hachiko statue, or the Magnet by Shibuya109 rooftop for the best views.",
    "rate": 5,
    "updatedAt": "2025-04-05T19:30:00Z"
  },
  {
    "locationId": 10,
    "creator": 3,
    "url": "https://www.youtube.com/watch?v=E5eGoKd2wQs",
    "review": "Attending a Geisha performance offers a unique opportunity to experience Japanese culture. Remember to make a reservation in advance and always ask for permission before taking photos.",
    "rate": 4,
    "updatedAt": "2025-04-05T19:30:00Z"
  },
  {
    "locationId": 11,
    "creator": 3,
    "url": "https://www.youtube.com/watch?v=E5eGoKd2wQs",
    "review": "Omakase Sushi is a must-try! Let the chef select and prepare a variety of sushi for you. It's okay to eat with your hands, and no need to dip in soy sauce.",
    "rate": 5,
    "updatedAt": "2025-04-05T19:30:00Z"
  },
  {
    "locationId": 12,
    "creator": 3,
    "url": "https://www.youtube.com/watch?v=E5eGoKd2wQs",
    "review": "Tsukiji Outer Market is the best for street food in Tokyo. Avoid weekends, and go early around 9:00 AM for fewer crowds. You might even find discounts around 1:00 PM!",
    "rate": 5,
    "updatedAt": "2025-04-05T19:30:00Z"
  },
  {
    "locationId": 13,
    "creator": 3,
    "url": "https://www.youtube.com/watch?v=E5eGoKd2wQs",
    "review": "Ueno offers so much! Explore Ueno Park during the day and head to Ameya Yokocho for street food and souvenirs at night. It's a fantastic place to experience Tokyo's energy.",
    "rate": 5,
    "updatedAt": "2025-04-05T19:30:00Z"
  },
  {
    "locationId": 1,
    "creator": 3,
    "url": "https://www.youtube.com/watch?v=E5eGoKd2wQs",
    "review": "Visit Sensoji and Kaminarimon is one of the most iconic spots in Tokyo. Tourists from Japan and overseas take great photos every day.",
    "rate": 5,
    "updatedAt": "2025-04-05T19:30:00Z"
  }
];

const additionalDummyLocations: Location[] = [
  {
    "id": "8",
    "name": "Shibuya Sky",
    "address": "2-24-12 Shibuya, Tokyo 150-6145, Japan",
    "category": "attraction",
    "coordinates": { "lat": 35.6585, "lng": 139.7012 },
    "business_hours": ["10:00-22:30"],
    "price_level": 4,
    "photos": ["https://lh3.googleusercontent.com/gps-cs-s/AB5caB9ZJFy3wTph2My-h5jY557c_tye19XQVI4XM-zcFergu4FphFY94t-UtqJbX3iaJNkt7WK722pqVX_so-mORY30P-XY2QDiNvieLtstZPHkEdxMsnByjreVuGNopMXGq5Bl0itBlQ=w270-h312-n-k-no"],
    "description": "Observation deck offering panoramic views of Tokyo, including Shibuya Crossing and Mt. Fuji.",
    "tags": ["observation deck", "panoramic view"],
    "reviews": [dummyLocationReviews[0]],
    "created_at": "2023-01-01T00:00:00Z"
  },
  {
    "id": "9",
    "name": "Shibuya Crossing",
    "address": "2-2-1 Dogenzaka, Shibuya, Tokyo 150-0043, Japan",
    "category": "attraction",
    "coordinates": { "lat": 35.6596, "lng": 139.7007 },
    "business_hours": ["24/7"],
    "price_level": 1,
    "photos": ["https://lh3.googleusercontent.com/gps-cs-s/AB5caB-Ik7UXvfQInITtBEMdDGmYEXctlVJ6mPdT-bAT2nDBLA-Fi9mJdEcFUhDfM8OB6qGcO2FjV4BVgDw9C3IZ21gadJtJfyfkU80BIWmnnlgLWmw2Qk6Z_kqDhFAhtveayO-EB1Oagw=w270-h156-n-k-no"],
    "description": "The world's busiest intersection, a must-see in Tokyo.",
    "tags": ["intersection", "iconic"],
    "reviews": [dummyLocationReviews[1]],
    "created_at": "2023-01-01T00:00:00Z"
  },
  {
    "id": "10",
    "name": "Gisha District",
    "address": "Various locations in Tokyo",
    "category": "attraction",
    "coordinates": { "lat": 35.6895, "lng": 139.6917 },
    "business_hours": ["Varies"],
    "price_level": 5,
    "photos": ["https://www.japan-guide.com/g18/3902_top.jpg"],
    "description": "Experience the traditional Japanese entertainers.",
    "tags": ["culture", "traditional performance"],
    "reviews": [dummyLocationReviews[2]],
    "created_at": "2023-01-01T00:00:00Z"
  },
  {
    "id": "12",
    "name": "Tsukiji Outer Market",
    "address": "4-16-2 Tsukiji, Tokyo 104-0045, Japan",
    "category": "restaurant",
    "coordinates": { "lat": 35.6659, "lng": 139.7693 },
    "business_hours": ["Varies"],
    "price_level": 2,
    "photos": ["https://www.japan-guide.com/g18/740/3021_05.jpg"],
    "description": "A bustling marketplace known for its fresh seafood and street food.",
    "tags": ["seafood", "street food", "market"],
    "reviews": [dummyLocationReviews[4]],
    "created_at": "2023-01-01T00:00:00Z"
  },
  {
    "id": "13",
    "name": "Ueno Park",
    "address": "Uenokoen, Taito, Tokyo 110-0007, Japan",
    "category": "attraction",
    "coordinates": { "lat": 35.7141, "lng": 139.7774 },
    "business_hours": ["5:00-23:00"],
    "price_level": 1,
    "photos": ["https://lh3.googleusercontent.com/gps-cs-s/AB5caB-kV9wgMgtZinMCBnaD-pHt1xgtDaeTk1Bh9904xLlZRanAdDht4SKyNrkpzVDdU_KzRUvTu7_OXLbtztw_uwnEmTTDxMP0G1_SuMrDuDneoovp1UMIMUg_cPTuTacjKMLIzUNv=s680-w680-h510"],
    "description": "A large public park in Tokyo known for its museums, temples, and zoo.",
    "tags": ["park", "museums", "zoo"],
    "reviews": [dummyLocationReviews[5]],
    "created_at": "2023-01-01T00:00:00Z"
  }
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
