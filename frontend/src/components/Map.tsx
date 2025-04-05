"use client";

import { useEffect, useRef, useState } from "react";
import { Location } from "../types/location";

// Helper function to create SVG marker content
const createSVGMarker = (iconPath: string, color: string) => {
  return `
    <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="20" cy="20" r="18" fill="white"/>
      <circle cx="20" cy="20" r="16" fill="${color}"/>
      <path d="${iconPath}" fill="white" transform="translate(12, 12) scale(0.67)"/>
    </svg>
  `;
};

// Star marker for suggested locations
const createStarMarker = (color: string) => {
  return `
    <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="20" cy="20" r="18" fill="white"/>
      <circle cx="20" cy="20" r="16" fill="${color}"/>
      <path d="M20 11l2.47 7.6h8l-6.47 4.72 2.47 7.6-6.47-4.72-6.47 4.72 2.47-7.6-6.47-4.72h8z" fill="white"/>
    </svg>
  `;
};



interface MapComponentProps {
  locations?: Location[];
  suggestedLocations?: Location[];
  onMapLoad?: (map: google.maps.Map) => void;
  onShowSuggestedLocations?: (location: Location) => void;
}

export default function MapComponent({ 
  locations = [], 
  suggestedLocations = [],
  onMapLoad, 
  onShowSuggestedLocations 
}: MapComponentProps) {
  const [map, setMap] = useState<google.maps.Map | null>(null);
  const [suggestedMarkers, setSuggestedMarkers] = useState<google.maps.marker.AdvancedMarkerElement[]>([]);
  const ref = useRef<HTMLDivElement>(null);
  const markersRef = useRef<google.maps.marker.AdvancedMarkerElement[]>([]);
  const infoWindowRef = useRef<google.maps.InfoWindow | null>(null);

  // Function to show suggested locations
  const showSuggestedLocations = (centerLocation: Location) => {
    // Clear existing suggested markers
    suggestedMarkers.forEach(marker => marker.map = null);

    // Create new markers for suggested locations
    const newSuggestedMarkers = suggestedLocations.map(location => {
      const marker = new google.maps.marker.AdvancedMarkerElement({
        map,
        position: { lat: location.coordinates.lat, lng: location.coordinates.lng },
        content: buildSuggestedMarkerContent(location),
        title: location.name,
      });

      // Add click listener for info window
      marker.addListener('click', () => {
        if (infoWindowRef.current) {
          infoWindowRef.current.setContent(buildInfoWindowContent(location));
          infoWindowRef.current.open(map, marker);
        }
      });

      return marker;
    });

    setSuggestedMarkers(newSuggestedMarkers);

    // Fit bounds to include both the clicked location and suggested locations
    if (map) {
      const bounds = new google.maps.LatLngBounds();
      bounds.extend({ lat: centerLocation.coordinates.lat, lng: centerLocation.coordinates.lng });
      suggestedLocations.forEach(location => {
        bounds.extend({ lat: location.coordinates.lat, lng: location.coordinates.lng });
      });
      map.fitBounds(bounds);
    }
  };

  useEffect(() => {
    if (!window.google || !ref.current) return;

    const initializeMap = () => {
      const defaultCenter = locations.length > 0 ? {
        lat: locations[0].coordinates.lat,
        lng: locations[0].coordinates.lng
      } : { lat: 0, lng: 0 };

      const newMap = new window.google.maps.Map(ref.current, {
        center: defaultCenter,
        zoom: 15,
        mapTypeControl: false,
        streetViewControl: false,
        mapId: "c977c19ab0823e14"
      });

      // Initialize InfoWindow
      infoWindowRef.current = new google.maps.InfoWindow();

      setMap(newMap);
      if (onMapLoad) onMapLoad(newMap);
      return newMap;
    };

    const currentMap = map || initializeMap();

    // Add event listener for showing suggested locations
    const handleShowSuggested = (e: CustomEvent<Location>) => {
      if (currentMap) {
        showSuggestedLocations(e.detail);
      }
    };

    window.addEventListener('showSuggestedLocations', handleShowSuggested as EventListener);

    // Clear existing markers
    markersRef.current.forEach(marker => marker.map = null);
    markersRef.current = [];

    // Add new markers
    locations.forEach(location => {
      const marker = new google.maps.marker.AdvancedMarkerElement({
        map: currentMap,
        position: { lat: location.coordinates.lat, lng: location.coordinates.lng },
        content: buildMarkerContent(location),
        title: location.name,
      });

      // Add click listener for info window and suggested locations
      marker.addListener('click', () => {
        if (infoWindowRef.current) {
          infoWindowRef.current.setContent(buildInfoWindowContent(location));
          infoWindowRef.current.open(currentMap, marker);
          showSuggestedLocations(location);
        }
      });

      markersRef.current.push(marker);
    });

    // Fit bounds if there are locations
    if (locations.length > 0) {
      const bounds = new google.maps.LatLngBounds();
      locations.forEach(location => {
        bounds.extend({ lat: location.coordinates.lat, lng: location.coordinates.lng });
      });
      currentMap.fitBounds(bounds);
    }

    return () => {
      window.removeEventListener('showSuggestedLocations', handleShowSuggested as EventListener);
    };
  }, [locations, onMapLoad, suggestedLocations]);

  // Helper function to build marker content
  const buildMarkerContent = (location: Location) => {
    let iconPath: string;
    let color: string;

    switch (location.category) {
      case 'attraction':
        // Place icon path
        iconPath = "M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z";
        color = "#f44336"; // Red
        break;
      case 'restaurant':
        // Restaurant icon path
        iconPath = "M11 9H9V2H7v7H5V2H3v7c0 2.12 1.66 3.84 3.75 3.97V22h2.5v-9.03C11.34 12.84 13 11.12 13 9V2h-2v7zm5-3v8h2.5v8H21V2c-2.76 0-5 2.24-5 4z";
        color = "#000000"; // Black
        break;
      case 'hotel':
        // Hotel icon path
        iconPath = "M7 13c1.66 0 3-1.34 3-3S8.66 7 7 7s-3 1.34-3 3 1.34 3 3 3zm12-6h-8v7H3V5H1v15h2v-3h18v3h2v-9c0-2.21-1.79-4-4-4z";
        color = "#4caf50"; // Green
        break;
      default:
        // Default location icon
        iconPath = "M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7z";
        color = "#757575"; // Grey
    }

    const markerSvg = createSVGMarker(iconPath, color);
    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(markerSvg, 'image/svg+xml');
    return svgDoc.documentElement;
  };

  // Helper function to build suggested marker content
  const buildSuggestedMarkerContent = (location: Location) => {
    const markerSvg = createStarMarker("#FFD700"); // Yellow color for suggested locations
    const parser = new DOMParser();
    const svgDoc = parser.parseFromString(markerSvg, 'image/svg+xml');
    return svgDoc.documentElement;
  };

  // Helper function to build info window content
  const buildInfoWindowContent = (location: Location) => {
    const ratingStars = location.rating ? '⭐'.repeat(Math.round(location.rating)) : '';
    const priceLevel = location.price_level ? '$'.repeat(location.price_level) : '';
    
    return `
      <div style="padding: 12px; max-width: 300px; font-family: Arial, sans-serif;">
        ${location.photos?.[0] ? `
          <div style="margin-bottom: 12px;">
            <img src="${location.photos[0]}" alt="${location.name}" 
                 style="width: 100%; height: 150px; object-fit: cover; border-radius: 4px;">
          </div>
        ` : ''}
        <h3 style="margin: 0 0 8px 0; font-size: 18px; color: #1976d2;">${location.name}</h3>
        <p style="margin: 0 0 8px 0; font-size: 14px; color: #666;">
          ${location.address}
        </p>
        ${location.business_hours ? `
          <p style="margin: 4px 0; font-size: 14px;">
            <strong>Hours:</strong> ${location.business_hours.join(', ')}
          </p>
        ` : ''}
        ${ratingStars ? `
          <p style="margin: 4px 0; font-size: 14px;">
            <strong>Rating:</strong> ${ratingStars} (${location.rating})
          </p>
        ` : ''}
        ${priceLevel ? `
          <p style="margin: 4px 0; font-size: 14px;">
            <strong>Price:</strong> ${priceLevel}
          </p>
        ` : ''}
        ${location.description ? `
          <p style="margin: 8px 0; font-size: 14px; color: #444;">
            ${location.description}
          </p>
        ` : ''}
        ${location.tags?.length ? `
          <div style="margin-top: 8px;">
            ${location.tags.map(tag => `
              <span style="display: inline-block; background: #e0e0e0; color: #666;
                         padding: 4px 8px; border-radius: 12px; font-size: 12px;
                         margin: 2px 4px 2px 0;">
                ${tag}
              </span>
            `).join('')}
          </div>
        ` : ''}
        ${suggestedLocations?.length ? `
          <div style="margin-top: 16px; border-top: 1px solid #e0e0e0; padding-top: 12px;">
            <p style="margin: 0 0 8px 0; font-size: 14px; font-weight: bold; color: #1976d2;">
              <span style="color: #ffd700;">★</span> Suggested Places Nearby:
            </p>
            <div style="max-height: 120px; overflow-y: auto;">
              ${suggestedLocations.map(suggested => `
                <div style="margin-bottom: 8px; padding: 8px; background: #f5f5f5; border-radius: 4px;">
                  <div style="font-size: 13px; font-weight: bold; color: #333;">
                    ${suggested.name}
                  </div>
                  <div style="font-size: 12px; color: #666; margin-top: 4px;">
                    ${suggested.description || ''}
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        ` : ''}
      </div>
    `;
  };

  return (
    <div
      ref={ref}
      style={{
        height: "100%",
        width: "100%",
        minHeight: "700px",
        borderRadius: "8px"
      }}
    />
  );
}
