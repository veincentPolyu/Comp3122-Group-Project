import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export interface Location {
  id: string;
  name: string;
  address: string;
  category: string;
  coordinates: {
    lat: number;
    lng: number;
  };
  businessHours?: string[];
  busyPeriods?: string[];
}

// Mock data for testing
const mockLocations: Location[] = [
  {
    id: "1",
    name: "Eiffel Tower",
    address: "Champ de Mars, 5 Avenue Anatole France, 75007 Paris, France",
    category: "attraction",
    coordinates: {
      lat: 48.8584,
      lng: 2.2945
    },
    businessHours: ["9:00 AM - 12:00 AM"],
    busyPeriods: ["10:00 AM - 2:00 PM", "6:00 PM - 8:00 PM"]
  },
  {
    id: "2",
    name: "Louvre Museum",
    address: "Rue de Rivoli, 75001 Paris, France",
    category: "museum",
    coordinates: {
      lat: 48.8606,
      lng: 2.3376
    },
    businessHours: ["9:00 AM - 6:00 PM"],
    busyPeriods: ["11:00 AM - 3:00 PM"]
  }
];

export const processUrl = async (url: string) => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 1000));
  return { status: "completed", locations: mockLocations };
};

export const getLocationDetails = async (placeId: string) => {
  await new Promise(resolve => setTimeout(resolve, 500));
  return mockLocations.find(loc => loc.id === placeId);
};
