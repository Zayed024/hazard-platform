import React from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Dashboard from './components/Dashboard/Dashboard';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2', // Blue for water/flood themes
      light: '#42a5f5',
      dark: '#1565c0'
    },
    secondary: {
      main: '#dc004e', // Red for alerts
      light: '#ff5983',
      dark: '#9a0036'
    },
    success: {
      main: '#4caf50',
      light: '#81c784',
      dark: '#388e3c'
    },
    warning: {
      main: '#ff9800',
      light: '#ffb74d', 
      dark: '#f57c00'
    },
    error: {
      main: '#f44336',
      light: '#e57373',
      dark: '#d32f2f'
    },
    info: {
      main: '#2196f3',
      light: '#64b5f6',
      dark: '#1976d2'
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff'
    }
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
      fontSize: '2.125rem',
      lineHeight: 1.235
    },
    h6: {
      fontWeight: 500,
      fontSize: '1.25rem',
      lineHeight: 1.6
    }
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
        }
      }
    },
    MuiPaper: {
      styleOverrides: {
        root: {
          borderRadius: '12px',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)'
        }
      }
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: '16px'
        }
      }
    }
  }
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="App" style={{ minHeight: '100vh', backgroundColor: theme.palette.background.default }}>
        <Dashboard />
      </div>
    </ThemeProvider>
  );
}

export default App;