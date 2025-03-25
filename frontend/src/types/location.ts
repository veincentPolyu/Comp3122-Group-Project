export interface Coordinates {
  lat: number;
  lng: number;
}

export interface ContentSource {
  url: string;
  type: string;
  title?: string;
  timestamp?: string;
}

export interface Location {
  id: string;
  name: string;
  address: string;
  category: string;
  coordinates: Coordinates;
  business_hours?: string[];
  busy_periods?: string[];
  rating?: number;
  price_level?: number;
  photos?: string[];
  description?: string;
  source?: ContentSource;
  tags?: string[];
  created_at: string;
}
