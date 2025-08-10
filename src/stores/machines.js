import { defineStore } from 'pinia'
import axios from 'axios'

export const useMachinesStore = defineStore('machines', {
  state: () => ({
    machines: [],
    loading: false,
    error: null,
    filters: {
      os: '',
      status: '',
      search: ''
    }
  }),

  getters: {
    filteredMachines: (state) => {
      let filtered = state.machines

      if (state.filters.os) {
        filtered = filtered.filter(machine => 
          machine.operating_system.toLowerCase().includes(state.filters.os.toLowerCase())
        )
      }

      if (state.filters.status) {
        filtered = filtered.filter(machine => 
          machine.status === state.filters.status
        )
      }

      if (state.filters.search) {
        filtered = filtered.filter(machine => 
          machine.hostname.toLowerCase().includes(state.filters.search.toLowerCase()) ||
          machine.machine_id.toLowerCase().includes(state.filters.search.toLowerCase())
        )
      }

      return filtered
    },

    machinesByStatus: (state) => {
      const statusCounts = {
        healthy: 0,
        warning: 0,
        critical: 0,
        offline: 0
      }

      state.machines.forEach(machine => {
        if (machine.last_check_in && Date.now() - new Date(machine.last_check_in).getTime() > 3600000) {
          statusCounts.offline++
        } else if (machine.issues && machine.issues.length > 0) {
          if (machine.issues.some(issue => issue.severity === 'critical')) {
            statusCounts.critical++
          } else {
            statusCounts.warning++
          }
        } else {
          statusCounts.healthy++
        }
      })

      return statusCounts
    }
  },

  actions: {
    async fetchMachines() {
      this.loading = true
      this.error = null
      
      try {
        const response = await axios.get('/api/machines')
        this.machines = response.data
      } catch (error) {
        this.error = 'Failed to fetch machines'
        console.error('Error fetching machines:', error)
      } finally {
        this.loading = false
      }
    },

    async fetchMachineById(machineId) {
      try {
        const response = await axios.get(`/api/machines/${machineId}`)
        return response.data
      } catch (error) {
        console.error('Error fetching machine:', error)
        throw error
      }
    },

    setFilter(filterType, value) {
      this.filters[filterType] = value
    },

    clearFilters() {
      this.filters = {
        os: '',
        status: '',
        search: ''
      }
    }
  }
})
