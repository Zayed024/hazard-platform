import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default markers
// @ts-ignore
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
});

interface Hazard {
  id: number;
  title: string;
  hazard_type: string;
  severity_score: number;
  trust_score: number;
  latitude: number;
  longitude: number;
}

interface HazardMapProps {
  hazards: Hazard[];
}


const HazardMap: React.FC<HazardMapProps> = ({ hazards }) => { 
  
  

  const getMarkerColor = (hazardType: string) => {
    switch (hazardType) {
      case 'flood': return '#2196F3'; // Blue
      case 'infrastructure': return '#FF9800'; // Orange
      case 'weather': return '#F44336'; // Red
      default: return '#9E9E9E'; // Gray
    }
  };

  return (
    <MapContainer 
      center={[13.0827, 80.2707]} 
      zoom={12} 
      style={{ height: '500px', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      />
      {hazards.map((hazard) => (
        <React.Fragment key={hazard.id}>
          <Marker position={[hazard.latitude, hazard.longitude]}>
            <Popup>
              <div style={{ minWidth: '200px' }}>
                <h4 style={{ margin: '0 0 8px 0', color: getMarkerColor(hazard.hazard_type) }}>
                  {hazard.title}
                </h4>
                <p><strong>Type:</strong> {hazard.hazard_type}</p>
                <p><strong>Severity:</strong> {(hazard.severity_score * 100).toFixed(0)}%</p>
                <p><strong>Trust Score:</strong> {(hazard.trust_score * 100).toFixed(0)}%</p>
                <div style={{ 
                  marginTop: '8px', 
                  padding: '4px 8px', 
                  borderRadius: '4px',
                  backgroundColor: hazard.severity_score > 0.7 ? '#ffebee' : '#e8f5e8',
                  color: hazard.severity_score > 0.7 ? '#c62828' : '#2e7d32',
                  fontSize: '12px'
                }}>
                  {hazard.severity_score > 0.7 ? '⚠️ High Priority' : '✓ Moderate'}
                </div>
              </div>
            </Popup>
          </Marker>
          <Circle
            center={[hazard.latitude, hazard.longitude]}
            radius={hazard.severity_score * 1000}
            fillColor={getMarkerColor(hazard.hazard_type)}
            fillOpacity={0.2}
            stroke={true}
            color={getMarkerColor(hazard.hazard_type)}
            weight={2}
          />
        </React.Fragment>
      ))}
    </MapContainer>
  );
};

export default HazardMap;