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
import HazardMap from './HazardMap';

interface DashboardStats {
  totalReports: number;
  activeHazards: number;
  verifiedReports: number;
  avgTrustScore: number;
  hazardTypes: {
    flood: number;
    infrastructure: number;
    weather: number;
    other: number;
  };
}

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call to fetch dashboard data
    const fetchDashboardData = async () => {
      try {
        // Mock data - replace with actual API call
        setTimeout(() => {
          setStats({
            totalReports: 1247,
            activeHazards: 23,
            verifiedReports: 891,
            avgTrustScore: 0.73,
            hazardTypes: {
              flood: 45,
              infrastructure: 12,
              weather: 8,
              other: 15
            }
          });
          setLoading(false);
        }, 1000);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        setLoading(false);
      }
    };

    fetchDashboardData();
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
            value={stats?.totalReports.toLocaleString() || 0}
            icon={<TrendingIcon sx={{ fontSize: 40 }} />}
            color="primary.main"
            subtitle="All time submissions"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Active Hazards"
            value={stats?.activeHazards || 0}
            icon={<WarningIcon sx={{ fontSize: 40 }} />}
            color="warning.main"
            subtitle="Requiring attention"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Verified Reports"
            value={stats?.verifiedReports.toLocaleString() || 0}
            icon={<VerifiedIcon sx={{ fontSize: 40 }} />}
            color="success.main"
            subtitle="Quality assured"
          />
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Avg Trust Score"
            value={`${((stats?.avgTrustScore || 0) * 100).toFixed(0)}%`}
            icon={<CheckCircle sx={{ fontSize: 40 }} />}
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
              {stats && Object.entries(stats.hazardTypes).map(([type, count]) => {
                const icons = {
                  flood: <FloodIcon sx={{ fontSize: 20 }} />,
                  infrastructure: <InfraIcon sx={{ fontSize: 20 }} />,
                  weather: <WeatherIcon sx={{ fontSize: 20 }} />,
                  other: <WarningIcon sx={{ fontSize: 20 }} />
                };
                
                const colors = {
                  flood: 'primary',
                  infrastructure: 'warning', 
                  weather: 'error',
                  other: 'default'
                } as const;

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
            <HazardMap />
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