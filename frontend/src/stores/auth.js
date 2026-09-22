import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useStorage } from '@vueuse/core'
import { apiClient } from '@/services/axios'
import { useRouter } from 'vue-router'
// import { useCookies } from '@vueuse/integrations/useCookies'

export const useAuthStore = defineStore(
  'auth',
  () => {
    const isLoggedIn = useStorage('isLoggedIn', false) // persist user in localStorage
    const loading = ref(false)

    const userInitialien = useStorage('userInitialien')

    const userRolleId = useStorage('userRolleId', null, undefined, {
      serializer: {
        read: (v) => (v === 'none' ? null : Number(v)),
        write: (v) => String(v)
      }
    })

    const gemeindeId = useStorage('gemeindeId', null, undefined, {
      serializer: {
        read: (v) => (v === 'none' ? null : Number(v)),
        write: (v) => String(v)
      }
    })

    const userId = useStorage('userId')
    const userEmail = useStorage('userEmail')
    const isVerified = useStorage('isVerified', false)

    const router = useRouter()

    async function register(data) {
      loading.value = true
      await apiClient.post('/auth/register', data)
      loading.value = false
    }

    async function login({ email, password }) {
      loading.value = true

      const formData = new FormData()
      formData.set('username', email)
      formData.set('password', password)

      const response = await apiClient.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      if (response.status === 204) {
        isLoggedIn.value = true // Set logged-in status if successful
        const user = await getUser()
        userInitialien.value =
          user.vorname.charAt(0).toUpperCase() + user.nachname.charAt(0).toUpperCase()
        userRolleId.value = user.rolleId
        gemeindeId.value = user.gemeindeId
        userId.value = user.id
        userEmail.value = user.email
        isVerified.value = user.isVerified
        if (user.rolleId === 3) {
          router.replace({ name: 'admin-kommunen' })
        } else {
          router.replace({ name: 'magistratsvorlage-liste' })
        }
      } else {
        isLoggedIn.value = false
      }
      loading.value = false
    }

    async function logout() {
      try {
        loading.value = true

        await apiClient.post('/auth/logout')
        isLoggedIn.value = false
        isVerified.value = false
        userRolleId.value = null
        router.replace({ name: 'startseite' })
      } catch (error) {
        if (error instanceof Error) {
          alert(error.message)
        }
      } finally {
        loading.value = false
      }
    }

    async function getUser() {
      try {
        const user = await apiClient.get('/users/me')
        return user.data
      } catch (error) {
        if (error instanceof Error) {
          console.log(error.message)
        }
      }
    }

    async function refreshVerified() {
      const user = await getUser()
      if (user) {
        isVerified.value = user.isVerified
      }
    }

    apiClient.interceptors.response.use(
      (response) => response, // Pass through if response is successful
      (error) => {
        if (error.response && error.response.status === 401 && isLoggedIn.value) {
          // Only redirect to login if the user had an active session
          router.replace({ name: 'anmelden', query: { redirect: 'sessionExpired' } })
          isLoggedIn.value = false
          userRolleId.value = null
        }
        // return Promise.reject(error) // Continue to reject the error to handle it locally if needed
      }
    )

    async function checkAuthStatus() {
      try {
        const response = await apiClient.get('/auth/status')
        if (response.status === 200) {
          isLoggedIn.value = true
        }
      } catch (error) {
        if (error.response && error.response.status === 401) {
          isLoggedIn.value = false // Logs the user out if the session expired
          // Optionally redirect to login
        }
      }
    }

    // setInterval(checkAuthStatus, 300000) // Check every 5 minutes

    async function updateUser(data) {
      try {
        loading.value = true
        await apiClient.patch('/users/me', data)
        loading.value = false
      } catch (error) {
        if (error instanceof Error) {
          alert(error.message)
        }
      }
    }

    async function forgotPassword(email) {
      try {
        loading.value = true
        await apiClient.post('/auth/forgot-password', { email })
        loading.value = false
      } catch (error) {
        if (error instanceof Error) {
          console.log(error.message)
        }
      }
    }

    async function resetPassword(token, password) {
      try {
        loading.value = true
        await apiClient.post('/auth/reset-password', { token, password })
        loading.value = false
      } catch (error) {
        if (error instanceof Error) {
          console.log(error.message)
        }
      }
    }

    return {
      loading,
      isLoggedIn,
      isVerified,
      userInitialien,
      gemeindeId,
      userId,
      userRolleId,
      userEmail,
      register,
      login,
      logout,
      checkAuthStatus,
      getUser,
      refreshVerified,
      updateUser,
      forgotPassword,
      resetPassword
    }
  }
  // ,
  // {
  //   persist: {
  //     storage: sessionStorage,
  //     paths: ['authState']
  //   }
  // }
)
