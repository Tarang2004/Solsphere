<template>
  <div class="px-4 sm:px-6 lg:px-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Dashboard</h1>
      <p class="mt-2 text-sm text-gray-600">
        Overview of all monitored systems and their health status
      </p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-success-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-success-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Healthy Systems</p>
            <p class="text-2xl font-semibold text-gray-900">{{ statusCounts.healthy }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-warning-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-warning-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Warnings</p>
            <p class="text-2xl font-semibold text-gray-900">{{ statusCounts.warning }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-danger-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-danger-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Critical Issues</p>
            <p class="text-2xl font-semibold text-gray-900">{{ statusCounts.critical }}</p>
          </div>
        </div>
      </div>

      <div class="card">
        <div class="flex items-center">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192L5.636 18.364M12 2.25a9.75 9.75 0 100 19.5 9.75 9.75 0 000-19.5z" />
              </svg>
            </div>
          </div>
          <div class="ml-4">
            <p class="text-sm font-medium text-gray-500">Offline</p>
            <p class="text-2xl font-semibold text-gray-900">{{ statusCounts.offline }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="card">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
        <div class="space-y-4">
          <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start space-x-3">
            <div class="flex-shrink-0">
              <div class="w-2 h-2 rounded-full" :class="getStatusColor(activity.status)"></div>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm text-gray-900">{{ activity.message }}</p>
              <p class="text-xs text-gray-500">{{ formatTime(activity.timestamp) }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <h3 class="text-lg font-medium text-gray-900 mb-4">System Distribution</h3>
        <div class="space-y-3">
          <div v-for="os in osDistribution" :key="os.name" class="flex items-center justify-between">
            <span class="text-sm text-gray-600">{{ os.name }}</span>
            <div class="flex items-center space-x-2">
              <div class="w-20 bg-gray-200 rounded-full h-2">
                <div class="bg-primary-600 h-2 rounded-full" :style="{ width: os.percentage + '%' }"></div>
              </div>
              <span class="text-sm text-gray-900 w-8">{{ os.count }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { useMachinesStore } from '../stores/machines'
import { useDashboardStore } from '../stores/dashboard'

export default {
  name: 'Dashboard',
  setup() {
    const machinesStore = useMachinesStore()
    const dashboardStore = useDashboardStore()

    const statusCounts = computed(() => machinesStore.machinesByStatus)
    
    const recentActivity = computed(() => dashboardStore.recentActivity)

    const osDistribution = computed(() => dashboardStore.osDistribution)

    const getStatusColor = (status) => {
      const colors = {
        success: 'bg-success-500',
        warning: 'bg-warning-500',
        danger: 'bg-danger-500'
      }
      return colors[status] || 'bg-gray-500'
    }

    const formatTime = (timestamp) => {
      const now = new Date()
      const diff = now - timestamp
      const minutes = Math.floor(diff / 60000)
      
      if (minutes < 1) return 'Just now'
      if (minutes < 60) return `${minutes}m ago`
      const hours = Math.floor(minutes / 60)
      if (hours < 24) return `${hours}h ago`
      return timestamp.toLocaleDateString()
    }

    onMounted(async () => {
      await Promise.all([
        dashboardStore.fetchDashboardStats(),
        machinesStore.fetchMachines()
      ])
    })

    return {
      statusCounts,
      recentActivity,
      osDistribution,
      getStatusColor,
      formatTime
    }
  }
}
</script>
