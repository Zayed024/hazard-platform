// frontend/src/services/apiService.ts
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api'; // Your FastAPI backend

// Define TypeScript interfaces for our data
export interface Hazard {
  id: number;
  title: string;
  description: string;
  hazard_type: string;
  latitude: number;
  longitude: number;
  trust_score: number;
  report_source: string;
  timestamp: string;
  severity_score: number;
}

export interface DashboardStats {
  total_reports: number;
  active_hazards: number;
  verified_reports: number;
  avg_trust_score: number;
  hazard_types: {
    [key: string]: number;
  };
}

// Function to fetch all hazard reports for the map
export const getHazardReports = async (): Promise<Hazard[]> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/hazards/reports/`);
    return response.data;
  } catch (error) {
    console.error("Error fetching hazard reports:", error);
    return [];
  }
};

// Function to fetch the main dashboard analytics
export const getDashboardAnalytics = async (): Promise<DashboardStats | null> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/hazards/analytics/dashboard`);
    return response.data;
  } catch (error) {
    console.error("Error fetching dashboard analytics:", error);
    return null;
  }
};