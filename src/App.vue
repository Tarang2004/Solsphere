<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <h1 class="text-xl font-bold text-primary-600">Solsphere</h1>
            </div>
            <div class="hidden md:ml-6 md:flex md:space-x-8">
              <router-link 
                to="/" 
                class="text-gray-900 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
                active-class="text-primary-600 border-b-2 border-primary-600"
              >
                Dashboard
              </router-link>
              <router-link 
                to="/machines" 
                class="text-gray-900 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
                active-class="text-primary-600 border-b-2 border-primary-600"
              >
                Machines
              </router-link>
              <router-link 
                to="/reports" 
                class="text-gray-900 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
                active-class="text-primary-600 border-b-2 border-primary-600"
              >
                Reports
              </router-link>
            </div>
          </div>
          <div class="flex items-center">
            <div class="ml-3 relative">
              <div class="flex items-center space-x-4">
                <span class="text-sm text-gray-700">Admin</span>
                <div class="w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
                  <span class="text-white text-sm font-medium">A</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <router-view />
    </main>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>
