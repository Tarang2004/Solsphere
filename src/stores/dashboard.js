import { defineStore } from 'pinia'
import axios from 'axios'
import { config } from '../config'

// Create axios instance with base URL
const api = axios.create({
  baseURL: config.apiBaseUrl
})

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    stats: {
      totalMachines: 0,
      healthyMachines: 0,
      warningMachines: 0,
      criticalMachines: 0,
      offlineMachines: 0
    },
    compliance: {
      diskEncryption: 0,
      osUpdates: 0,
      antivirus: 0,
      sleepSettings: 0
    },
    recentActivity: [],
    osDistribution: [],
    loading: false,
    error: null
  }),

  getters: {
    compliancePercentage: (state) => {
      const total = Object.values(state.compliance).reduce((sum, count) => sum + count, 0)
      return total > 0 ? Math.round((state.compliance.diskEncryption + state.compliance.antivirus) / total * 100) : 0
    }
  },

  actions: {
    async fetchDashboardStats() {
      this.loading = true
      this.error = null
      
      try {
        const [statsResponse, complianceResponse] = await Promise.all([
          api.get('/api/dashboard/stats'),
          api.get('/api/dashboard/compliance')
        ])
        
        this.stats = statsResponse.data
        this.compliance = complianceResponse.data
        
        // Generate mock data for demo purposes
        this.generateMockData()
      } catch (error) {
        this.error = 'Failed to fetch dashboard data'
        console.error('Error fetching dashboard data:', error)
        // Generate mock data as fallback
        this.generateMockData()
      } finally {
        this.loading = false
      }
    },

    generateMockData() {
      // Mock recent activity
      this.recentActivity = [
        {
          id: 1,
          message: 'Machine WIN-ABC123 completed health check',
          status: 'healthy',
          timestamp: new Date(Date.now() - 5 * 60000).toISOString()
        },
        {
          id: 2,
          message: 'Machine MAC-DEF456 detected disk encryption issue',
          status: 'warning',
          timestamp: new Date(Date.now() - 15 * 60000).toISOString()
        },
        {
          id: 3,
          message: 'Machine LIN-GHI789 antivirus scan completed',
          status: 'healthy',
          timestamp: new Date(Date.now() - 30 * 60000).toISOString()
        }
      ]

      // Mock OS distribution
      this.osDistribution = [
        { name: 'Windows 11', count: 45, percentage: 45 },
        { name: 'Windows 10', count: 30, percentage: 30 },
        { name: 'macOS', count: 15, percentage: 15 },
        { name: 'Linux', count: 10, percentage: 10 }
      ]
    },

    async refreshData() {
      await this.fetchDashboardStats()
    }
  }
})
