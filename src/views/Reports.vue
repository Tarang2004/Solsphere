<template>
  <div class="px-4 sm:px-6 lg:px-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Reports</h1>
      <p class="mt-2 text-sm text-gray-600">
        Generate and export system health reports
      </p>
    </div>

    <!-- Report Generation -->
    <div class="card mb-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Generate Report</h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Report Type</label>
          <select
            v-model="reportType"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="overview">System Overview</option>
            <option value="health">Health Status</option>
            <option value="issues">Issues Summary</option>
            <option value="compliance">Compliance Report</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">Date Range</label>
          <select
            v-model="dateRange"
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          >
            <option value="7">Last 7 days</option>
            <option value="30">Last 30 days</option>
            <option value="90">Last 90 days</option>
            <option value="365">Last year</option>
          </select>
        </div>
        <div class="flex items-end">
          <button
            @click="generateReport"
            :disabled="generating"
            class="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="generating" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Generating...
            </span>
            <span v-else>Generate Report</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Quick Stats -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-5 mb-8">
      <div class="card">
        <div class="text-center">
          <p class="text-sm font-medium text-gray-500">Total Systems</p>
          <p class="text-2xl font-semibold text-gray-900">{{ quickStats.totalSystems }}</p>
        </div>
      </div>
      <div class="card">
        <div class="text-center">
          <p class="text-sm font-medium text-gray-500">Compliance Rate</p>
          <p class="text-2xl font-semibold text-gray-900">{{ quickStats.complianceRate }}%</p>
        </div>
      </div>
      <div class="card">
        <div class="text-center">
          <p class="text-sm font-medium text-gray-500">Active Issues</p>
          <p class="text-2xl font-semibold text-gray-900">{{ quickStats.activeIssues }}</p>
        </div>
      </div>
      <div class="card">
        <div class="text-center">
          <p class="text-sm font-medium text-gray-500">Last Report</p>
          <p class="text-sm text-gray-900">{{ quickStats.lastReport }}</p>
        </div>
      </div>
    </div>

    <!-- Compliance Overview -->
    <div class="card mb-6">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Compliance Overview</h3>
      <div class="space-y-4">
        <div v-for="check in complianceChecks" :key="check.name" class="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <div :class="getComplianceIcon(check.status)" class="w-6 h-6 rounded-full flex items-center justify-center">
                <svg v-if="check.status === 'compliant'" class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                <svg v-else-if="check.status === 'warning'" class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
                <svg v-else class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </div>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-gray-900">{{ check.name }}</p>
              <p class="text-sm text-gray-500">{{ check.description }}</p>
            </div>
          </div>
          <div class="text-right">
            <p class="text-sm font-medium" :class="getComplianceTextColor(check.status)">
              {{ check.complianceRate }}%
            </p>
            <p class="text-xs text-gray-500">{{ check.compliantCount }}/{{ check.totalCount }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Reports -->
    <div class="card">
      <h3 class="text-lg font-medium text-gray-900 mb-4">Recent Reports</h3>
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Report Name
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Generated
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="report in recentReports" :key="report.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm font-medium text-gray-900">{{ report.name }}</div>
                <div class="text-sm text-gray-500">{{ report.description }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex px-2 py-1 text-xs font-semibold rounded-full" :class="getReportTypeClass(report.type)">
                  {{ report.type }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ formatDate(report.generated) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                <button
                  @click="downloadReport(report)"
                  class="text-primary-600 hover:text-primary-900 mr-3"
                >
                  Download
                </button>
                <button
                  @click="deleteReport(report)"
                  class="text-red-600 hover:text-red-900"
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useMachinesStore } from '../stores/machines'

export default {
  name: 'Reports',
  setup() {
    const machinesStore = useMachinesStore()
    const reportType = ref('overview')
    const dateRange = ref('30')
    const generating = ref(false)

    const quickStats = computed(() => ({
      totalSystems: machinesStore.machines.length,
      complianceRate: calculateComplianceRate(),
      activeIssues: countActiveIssues(),
      lastReport: '2 hours ago'
    }))

    const complianceChecks = computed(() => [
      {
        name: 'Disk Encryption',
        description: 'All systems must have disk encryption enabled',
        status: getComplianceStatus('disk_encryption'),
        complianceRate: getComplianceRate('disk_encryption'),
        compliantCount: getCompliantCount('disk_encryption'),
        totalCount: machinesStore.machines.length
      },
      {
        name: 'OS Updates',
        description: 'Systems must be running latest OS version',
        status: getComplianceStatus('os_updates'),
        complianceRate: getComplianceRate('os_updates'),
        compliantCount: getCompliantCount('os_updates'),
        totalCount: machinesStore.machines.length
      },
      {
        name: 'Antivirus',
        description: 'All systems must have active antivirus protection',
        status: getComplianceStatus('antivirus'),
        complianceRate: getComplianceRate('antivirus'),
        compliantCount: getCompliantCount('antivirus'),
        totalCount: machinesStore.machines.length
      },
      {
        name: 'Sleep Settings',
        description: 'Inactivity sleep must be ≤ 10 minutes',
        status: getComplianceStatus('sleep_settings'),
        complianceRate: getComplianceRate('sleep_settings'),
        compliantCount: getCompliantCount('sleep_settings'),
        totalCount: machinesStore.machines.length
      }
    ])

    const recentReports = ref([
      {
        id: 1,
        name: 'Monthly Compliance Report',
        description: 'Comprehensive compliance overview for all systems',
        type: 'compliance',
        generated: new Date(Date.now() - 7200000)
      },
      {
        id: 2,
        name: 'System Health Summary',
        description: 'Current health status of all monitored systems',
        type: 'health',
        generated: new Date(Date.now() - 14400000)
      },
      {
        id: 3,
        name: 'Issues Report',
        description: 'Summary of all active system issues',
        type: 'issues',
        generated: new Date(Date.now() - 21600000)
      }
    ])

    const calculateComplianceRate = () => {
      if (machinesStore.machines.length === 0) return 0
      const totalChecks = machinesStore.machines.length * 4 // 4 compliance checks per machine
      const compliantChecks = machinesStore.machines.reduce((total, machine) => {
        let compliant = 0
        if (machine.disk_encrypted) compliant++
        if (machine.os_up_to_date) compliant++
        if (machine.antivirus_active) compliant++
        if (machine.sleep_settings_compliant) compliant++
        return total + compliant
      }, 0)
      return Math.round((compliantChecks / totalChecks) * 100)
    }

    const countActiveIssues = () => {
      return machinesStore.machines.reduce((total, machine) => {
        return total + (machine.issues?.length || 0)
      }, 0)
    }

    const getComplianceStatus = (checkType) => {
      const rate = getComplianceRate(checkType)
      if (rate >= 90) return 'compliant'
      if (rate >= 70) return 'warning'
      return 'non-compliant'
    }

    const getComplianceRate = (checkType) => {
      if (machinesStore.machines.length === 0) return 0
      const compliant = getCompliantCount(checkType)
      return Math.round((compliant / machinesStore.machines.length) * 100)
    }

    const getCompliantCount = (checkType) => {
      return machinesStore.machines.filter(machine => {
        switch (checkType) {
          case 'disk_encryption':
            return machine.disk_encrypted
          case 'os_updates':
            return machine.os_up_to_date
          case 'antivirus':
            return machine.antivirus_active
          case 'sleep_settings':
            return machine.sleep_settings_compliant
          default:
            return false
        }
      }).length
    }

    const getComplianceIcon = (status) => {
      const classes = {
        compliant: 'bg-success-500',
        warning: 'bg-warning-500',
        'non-compliant': 'bg-danger-500'
      }
      return classes[status] || 'bg-gray-500'
    }

    const getComplianceTextColor = (status) => {
      const classes = {
        compliant: 'text-success-600',
        warning: 'text-warning-600',
        'non-compliant': 'text-danger-600'
      }
      return classes[status] || 'text-gray-600'
    }

    const getReportTypeClass = (type) => {
      const classes = {
        compliance: 'bg-blue-100 text-blue-800',
        health: 'bg-green-100 text-green-800',
        issues: 'bg-yellow-100 text-yellow-800',
        overview: 'bg-gray-100 text-gray-800'
      }
      return classes[type] || 'bg-gray-100 text-gray-800'
    }

    const formatDate = (date) => {
      const now = new Date()
      const diff = now - date
      const minutes = Math.floor(diff / 60000)
      
      if (minutes < 1) return 'Just now'
      if (minutes < 60) return `${minutes}m ago`
      const hours = Math.floor(minutes / 60)
      if (hours < 24) return `${hours}h ago`
      return date.toLocaleDateString()
    }

    const generateReport = async () => {
      generating.value = true
      
      try {
        // Simulate report generation
        await new Promise(resolve => setTimeout(resolve, 2000))
        
        // Add new report to list
        const newReport = {
          id: Date.now(),
          name: `${reportType.value.charAt(0).toUpperCase() + reportType.value.slice(1)} Report`,
          description: `Generated ${dateRange.value} day report`,
          type: reportType.value,
          generated: new Date()
        }
        recentReports.value.unshift(newReport)
        
        // Show success message (in real app, would use toast notification)
        alert('Report generated successfully!')
      } catch (error) {
        console.error('Error generating report:', error)
        alert('Error generating report')
      } finally {
        generating.value = false
      }
    }

    const downloadReport = (report) => {
      // Simulate report download
      const data = {
        report: report,
        data: machinesStore.machines,
        generated: new Date().toISOString()
      }
      
      const dataStr = JSON.stringify(data, null, 2)
      const dataBlob = new Blob([dataStr], { type: 'application/json' })
      const url = URL.createObjectURL(dataBlob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${report.name.toLowerCase().replace(/\s+/g, '-')}-${Date.now()}.json`
      link.click()
      URL.revokeObjectURL(url)
    }

    const deleteReport = (report) => {
      if (confirm(`Are you sure you want to delete "${report.name}"?`)) {
        const index = recentReports.value.findIndex(r => r.id === report.id)
        if (index > -1) {
          recentReports.value.splice(index, 1)
        }
      }
    }

    onMounted(() => {
      machinesStore.fetchMachines()
    })

    return {
      reportType,
      dateRange,
      generating,
      quickStats,
      complianceChecks,
      recentReports,
      getComplianceIcon,
      getComplianceTextColor,
      getReportTypeClass,
      formatDate,
      generateReport,
      downloadReport,
      deleteReport
    }
  }
}
</script>
