<template>
  <div class="px-4 sm:px-6 lg:px-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Machines</h1>
      <p class="mt-2 text-sm text-gray-600">
        Monitor and manage all connected systems
      </p>
    </div>

    <!-- Filters -->
    <div class="card mb-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Search</label>
          <input
            v-model="machinesStore.filters.search"
            type="text"
            placeholder="Search machines..."
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Operating System</label>
          <select
            v-model="machinesStore.filters.os"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All OS</option>
            <option value="Windows">Windows</option>
            <option value="macOS">macOS</option>
            <option value="Linux">Linux</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
          <select
            v-model="machinesStore.filters.status"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="">All Status</option>
            <option value="healthy">Healthy</option>
            <option value="warning">Warning</option>
            <option value="critical">Critical</option>
            <option value="offline">Offline</option>
          </select>
        </div>
        <div class="flex items-end">
          <button
            @click="machinesStore.clearFilters()"
            class="btn-secondary w-full"
          >
            Clear Filters
          </button>
        </div>
      </div>
    </div>

    <!-- Machines Table -->
    <div class="card">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Machine
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                OS
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Last Check-in
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Issues
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-if="machinesStore.loading" class="animate-pulse">
              <td colspan="6" class="px-6 py-4">
                <div class="flex items-center justify-center">
                  <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
                  <span class="ml-2 text-gray-500">Loading machines...</span>
                </div>
              </td>
            </tr>
            <tr v-else-if="machinesStore.error" class="text-center">
              <td colspan="6" class="px-6 py-4 text-red-600">
                {{ machinesStore.error }}
              </td>
            </tr>
            <tr v-else-if="filteredMachines.length === 0" class="text-center">
              <td colspan="6" class="px-6 py-4 text-gray-500">
                No machines found matching the current filters.
              </td>
            </tr>
            <tr v-else v-for="machine in filteredMachines" :key="machine.machine_id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-10 w-10">
                    <div class="h-10 w-10 rounded-full bg-primary-100 flex items-center justify-center">
                      <span class="text-primary-600 font-medium text-sm">
                        {{ machine.hostname?.charAt(0)?.toUpperCase() || 'M' }}
                      </span>
                    </div>
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ machine.hostname }}</div>
                    <div class="text-sm text-gray-500">{{ machine.machine_id }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ machine.operating_system }}</div>
                <div class="text-sm text-gray-500">{{ machine.os_version }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span :class="getStatusClass(machine)">
                  {{ getStatusText(machine) }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ formatLastCheckIn(machine.last_check_in) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div v-if="machine.issues && machine.issues.length > 0" class="space-y-1">
                  <div v-for="issue in machine.issues.slice(0, 2)" :key="issue.id" class="text-xs">
                    <span :class="getIssueClass(issue.severity)">
                      {{ issue.message }}
                    </span>
                  </div>
                  <div v-if="machine.issues.length > 2" class="text-xs text-gray-500">
                    +{{ machine.issues.length - 2 }} more issues
                  </div>
                </div>
                <span v-else class="text-sm text-gray-500">No issues</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  @click="viewMachineDetails(machine)"
                  class="text-primary-600 hover:text-primary-900 mr-3"
                >
                  View
                </button>
                <button
                  @click="exportMachineData(machine)"
                  class="text-gray-600 hover:text-gray-900"
                >
                  Export
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Machine Details Modal -->
    <div v-if="selectedMachine" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
      <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
        <div class="mt-3">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg font-medium text-gray-900">Machine Details</h3>
            <button
              @click="selectedMachine = null"
              class="text-gray-400 hover:text-gray-600"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Hostname</label>
                <p class="text-sm text-gray-900">{{ selectedMachine.hostname }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Machine ID</label>
                <p class="text-sm text-gray-900">{{ selectedMachine.machine_id }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Operating System</label>
                <p class="text-sm text-gray-900">{{ selectedMachine.operating_system }} {{ selectedMachine.os_version }}</p>
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700">Last Check-in</label>
                <p class="text-sm text-gray-900">{{ formatLastCheckIn(selectedMachine.last_check_in) }}</p>
              </div>
            </div>
            
            <div v-if="selectedMachine.issues && selectedMachine.issues.length > 0">
              <label class="block text-sm font-medium text-gray-700 mb-2">Issues</label>
              <div class="space-y-2">
                <div v-for="issue in selectedMachine.issues" :key="issue.id" class="p-3 rounded-md" :class="getIssueBgClass(issue.severity)">
                  <div class="flex items-center justify-between">
                    <span class="text-sm font-medium" :class="getIssueTextClass(issue.severity)">
                      {{ issue.message }}
                    </span>
                    <span :class="getIssueClass(issue.severity)">
                      {{ issue.severity }}
                    </span>
                  </div>
                  <p v-if="issue.details" class="text-xs mt-1" :class="getIssueTextClass(issue.severity)">
                    {{ issue.details }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, onMounted } from 'vue'
import { useMachinesStore } from '../stores/machines'

export default {
  name: 'Machines',
  setup() {
    const machinesStore = useMachinesStore()
    const selectedMachine = ref(null)

    const filteredMachines = computed(() => machinesStore.filteredMachines)

    const getStatusClass = (machine) => {
      if (!machine.last_check_in || Date.now() - new Date(machine.last_check_in).getTime() > 3600000) {
        return 'status-danger'
      }
      if (machine.issues && machine.issues.some(issue => issue.severity === 'critical')) {
        return 'status-danger'
      }
      if (machine.issues && machine.issues.length > 0) {
        return 'status-warning'
      }
      return 'status-success'
    }

    const getStatusText = (machine) => {
      if (!machine.last_check_in || Date.now() - new Date(machine.last_check_in).getTime() > 3600000) {
        return 'Offline'
      }
      if (machine.issues && machine.issues.some(issue => issue.severity === 'critical')) {
        return 'Critical'
      }
      if (machine.issues && machine.issues.length > 0) {
        return 'Warning'
      }
      return 'Healthy'
    }

    const getIssueClass = (severity) => {
      const classes = {
        critical: 'status-danger',
        warning: 'status-warning',
        info: 'status-success'
      }
      return classes[severity] || 'status-success'
    }

    const getIssueBgClass = (severity) => {
      const classes = {
        critical: 'bg-danger-50',
        warning: 'bg-warning-50',
        info: 'bg-success-50'
      }
      return classes[severity] || 'bg-success-50'
    }

    const getIssueTextClass = (severity) => {
      const classes = {
        critical: 'text-danger-700',
        warning: 'text-warning-700',
        info: 'text-success-700'
      }
      return classes[severity] || 'text-success-700'
    }

    const formatLastCheckIn = (timestamp) => {
      if (!timestamp) return 'Never'
      const now = new Date()
      const lastCheck = new Date(timestamp)
      const diff = now - lastCheck
      const minutes = Math.floor(diff / 60000)
      
      if (minutes < 1) return 'Just now'
      if (minutes < 60) return `${minutes}m ago`
      const hours = Math.floor(minutes / 60)
      if (hours < 24) return `${hours}h ago`
      return lastCheck.toLocaleDateString()
    }

    const viewMachineDetails = (machine) => {
      selectedMachine.value = machine
    }

    const exportMachineData = (machine) => {
      const dataStr = JSON.stringify(machine, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${machine.hostname}-${machine.machine_id}.json`
      link.click()
      URL.revokeObjectURL(url)
    }

    onMounted(() => {
      machinesStore.fetchMachines()
    })

    return {
      machinesStore,
      selectedMachine,
      filteredMachines,
      getStatusClass,
      getStatusText,
      getIssueClass,
      getIssueBgClass,
      getIssueTextClass,
      formatLastCheckIn,
      viewMachineDetails,
      exportMachineData
    }
  }
}
</script>
