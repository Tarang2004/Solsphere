// Frontend configuration
export const config = {
  // API Configuration
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  
  // App Configuration
  appName: 'Solsphere',
  appVersion: '1.0.0',
  
  // Refresh intervals (in milliseconds)
  refreshIntervals: {
    dashboard: 30000,    // 30 seconds
    machines: 60000,     // 1 minute
    reports: 300000      // 5 minutes
  },
  
  // Status colors
  statusColors: {
    healthy: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    critical: 'bg-red-100 text-red-800',
    offline: 'bg-gray-100 text-gray-800'
  }
}

export default config
