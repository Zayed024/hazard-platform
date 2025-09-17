//synapse-hazard-platform\frontend\src\components\Dashboard\Dashboard.tsx
import React, { useState, useEffect } from 'react';
import { 
  Grid, 
  Paper, 
  Typography, 
  Box, 
  Chip, 
  Card, 
  CardContent,
  LinearProgress
} from '@mui/material';
import { 
  WaterDrop as FloodIcon,
  Warning as WarningIcon,
  Cloud as WeatherIcon,
  Engineering as InfraIcon,
  CheckCircle as VerifiedIcon,
  TrendingUp as TrendingIcon
} from '@mui/icons-material';
import { getDashboardAnalytics, getHazardReports, Hazard, DashboardStats } from '../../services/apiService'; // Import our new service and types
import HazardMap from './HazardMap';

// interface DashboardStats {
//   totalReports: number;
//   activeHazards: number;
//   verifiedReports: number;
//   avgTrustScore: number;
//   hazardTypes: {
//     flood: number;
//     infrastructure: number;
//     weather: number;
//     other: number;
//   };
// }

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [hazards, setHazards] = useState<Hazard[]>([]); // Add state for hazards
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // This now fetches REAL data from your backend
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        // Fetch both analytics and hazard reports in parallel
        const [analyticsData, reportsData] = await Promise.all([
          getDashboardAnalytics(),
          getHazardReports()
        ]);
        
        setStats(analyticsData);
        setHazards(reportsData);

      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();

     //Establish the WebSocket connection for real-time updates
    const ws = new WebSocket("ws://localhost:8000/ws/dashboard");

    ws.onopen = () => {
      console.log("WebSocket connection established for live updates.");
    };

    ws.onmessage = (event) => {
      try {
        const newReport: Hazard = JSON.parse(event.data);
        console.log("New live report received:", newReport);

        // Update the hazards list to add the new report at the top
        setHazards(prevHazards => [newReport, ...prevHazards]);

        // Update the statistics cards dynamically
         setStats(prevStats => {
          if (!prevStats) return null;
          
          const newHazardTypes = { ...prevStats.hazard_types };
          newHazardTypes[newReport.hazard_type] = (newHazardTypes[newReport.hazard_type] || 0) + 1;

          return {
            ...prevStats,
            total_reports: prevStats.total_reports + 1,
            active_hazards: prevStats.active_hazards + 1, // Assuming new reports are active
            hazard_types: newHazardTypes
          };
        });

      } catch (error) {
        console.error("Error processing WebSocket message:", error);
      }
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed.");
    };

    // 3. Clean up the connection when the component unmounts
    return () => {
      ws.close();
    };
        
  }, []);

  const StatCard: React.FC<{ 
    title: string; 
    value: string | number; 
    icon: React.ReactNode; 
    color: string;
    subtitle?: string;
  }> = ({ title, value, icon, color, subtitle }) => (
    <Card elevation={2} sx={{ height: '100%' }}>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography variant="h6" color="textSecondary" gutterBottom>
              {title}
            </Typography>
            <Typography variant="h4" component="h2" color={color}>
              {value}
            </Typography>
            {subtitle && (
              <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                {subtitle}
              </Typography>
            )}
          </Box>
          <Box sx={{ color, opacity: 0.7 }}>
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  if (loading) {
    return (
      <Box sx={{ width: '100%', p: 3 }}>
        <Typography variant="h4" gutterBottom>
          🌊 Synapse - Hazard Intelligence Dashboard
        </Typography>
        <LinearProgress sx={{ mt: 2 }} />
      </Box>
    );
  }

  return (
  <Box sx={{ flexGrow: 1, p: 3 }}>
    <Typography variant="h4" gutterBottom sx={{ mb: 3, fontWeight: 'bold' }}>
      🌊 Synapse - Hazard Intelligence Dashboard
    </Typography>
    
    <Grid container spacing={3}>
      {/* Stats Cards */}
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Total Reports"
          value={stats?.total_reports?.toLocaleString() || 0} // Use snake_case
          icon={<TrendingIcon sx={{ fontSize: 40 }} />}
          color="primary.main"
          subtitle="All time submissions"
        />
      </Grid>
      
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Active Hazards"
          value={stats?.active_hazards || 0} // Use snake_case
          icon={<WarningIcon sx={{ fontSize: 40 }} />}
          color="warning.main"
          subtitle="Requiring attention"
        />
      </Grid>
      
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Verified Reports"
          value={stats?.verified_reports?.toLocaleString() || 0} // Use snake_case
          icon={<VerifiedIcon sx={{ fontSize: 40 }} />}
          color="success.main"
          subtitle="Quality assured"
        />
      </Grid>
      
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Avg Trust Score"
          value={`${Math.round((stats?.avg_trust_score || 0) * 100)}%`} // Use snake_case
          icon={<VerifiedIcon sx={{ fontSize: 40 }} />}
          color="info.main"
          subtitle="AI confidence level"
        />
      </Grid>

        {/* Hazard Types Summary */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, height: 'fit-content' }}>
            <Typography variant="h6" gutterBottom>
              📊 Hazard Distribution
            </Typography>
            <Box sx={{ mt: 2 }}>
              {stats?.hazard_types && Object.entries(stats.hazard_types).map(([type, count]) => {
                const icons: Record<string, JSX.Element> = {
                flood: <FloodIcon sx={{ fontSize: 20 }} />,
                infrastructure: <InfraIcon sx={{ fontSize: 20 }} />,
                weather: <WeatherIcon sx={{ fontSize: 20 }} />,
                other: <WarningIcon sx={{ fontSize: 20 }} />
              };

              const colors: Record<string, 'primary' | 'warning' | 'error' | 'default'> = {
                flood: 'primary',
                infrastructure: 'warning',
                weather: 'error',
                other: 'default'
              };

                return (
                  <Box key={type} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      {icons[type as keyof typeof icons]}
                      <Typography variant="body1" sx={{ textTransform: 'capitalize' }}>
                        {type}
                      </Typography>
                    </Box>
                    <Chip 
                      label={count} 
                      color={colors[type as keyof typeof colors]}
                      size="small"
                    />
                  </Box>
                );
              })}
            </Box>
          </Paper>
        </Grid>

        {/* Map */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">🗺️ Real-time Hazard Map</Typography>
              <Box>
                <Chip label="🌊 Flood" color="primary" size="small" sx={{ mr: 1 }} />
                <Chip label="🌳 Infrastructure" color="warning" size="small" sx={{ mr: 1 }} />
                <Chip label="⛈️ Weather" color="error" size="small" />
              </Box>
            </Box>
            <HazardMap hazards={hazards} />
          </Paper>
        </Grid>

        {/* Recent Activity */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              📋 Recent Activity
            </Typography>
            <Box sx={{ mt: 2 }}>
              {[
                { time: '2 min ago', event: 'New flood report verified in Chennai Marina Beach', type: 'success' },
                { time: '5 min ago', event: 'Infrastructure hazard detected via social media analysis', type: 'warning' },
                { time: '12 min ago', event: 'Weather alert integrated from meteorological services', type: 'info' },
                { time: '1 hour ago', event: 'Trust score algorithm updated with new ML model', type: 'default' }
              ].map((activity, index) => (
                <Box key={index} sx={{ display: 'flex', alignItems: 'center', gap: 2, py: 1, borderBottom: index < 3 ? '1px solid #e0e0e0' : 'none' }}>
                  <Chip label={activity.time} size="small" color={activity.type as any} variant="outlined" />
                  <Typography variant="body2">{activity.event}</Typography>
                </Box>
              ))}
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;