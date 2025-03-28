"use client";

import { useEffect, useRef, useState } from "react";
import { Location } from "../types/location";

interface MapComponentProps {
  locations?: Location[];
  onMapLoad?: (map: google.maps.Map) => void;
}

export default function MapComponent({ locations = [], onMapLoad }: MapComponentProps) {
  const [map, setMap] = useState<google.maps.Map>();
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!window.google || !ref.current || !locations.length) return;

    if (!map) {
      const defaultCenter = {
        lat: locations[0].coordinates.lat,
        lng: locations[0].coordinates.lng
      };

      const newMap = new window.google.maps.Map(ref.current, {
        center: defaultCenter,
        zoom: 15,
        mapTypeControl: false,
        streetViewControl: false,
        mapId: "c977c19ab0823e14"
      });

      // Add advanced markers for each location
      locations.forEach(location => {
        const position = { 
          lat: location.coordinates.lat, 
          lng: location.coordinates.lng 
        };

        const markerView = new google.maps.marker.AdvancedMarkerElement({
          map: newMap,
          position: position,
          title: location.name,
          content: buildMarkerContent(location)
        });

        // Add click listener for info window
        markerView.addListener('click', () => {
          const infoWindow = new google.maps.InfoWindow({
            content: buildInfoWindowContent(location)
          });
          infoWindow.open(newMap, markerView);
        });
      });

      setMap(newMap);
      if (onMapLoad) onMapLoad(newMap);
    }
  }, [map, locations, onMapLoad]);

  // Helper function to build marker content
  const buildMarkerContent = (location: Location) => {
    const pin = new google.maps.marker.PinElement({
      background: location.category === 'attraction' ? '#1976d2' 
                 : location.category === 'restaurant' ? '#dc004e'
                 : '#4caf50',
      glyphColor: '#ffffff',
      borderColor: '#ffffff',
      scale: 1.2
    });
    return pin.element;
  };

  // Helper function to build info window content
  const buildInfoWindowContent = (location: Location) => {
    return `
      <div style="padding: 8px; max-width: 200px;">
        <h3 style="margin: 0 0 8px 0; font-size: 16px;">${location.name}</h3>
        <p style="margin: 0 0 4px 0; font-size: 14px; color: #666;">
          ${location.address}
        </p>
        ${location.rating ? 
          `<p style="margin: 4px 0; font-size: 14px;">
            Rating: ⭐${location.rating}
           </p>` 
          : ''}
        ${location.description ? 
          `<p style="margin: 4px 0; font-size: 13px; color: #666;">
            ${location.description}
           </p>` 
          : ''}
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