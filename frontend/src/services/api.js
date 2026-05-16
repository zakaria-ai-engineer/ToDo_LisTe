import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'https://todo-199jiuq4.b4a.run'

const api = axios.create({ baseURL: BASE_URL })

// ── REQUEST interceptor — injecte le JWT ──────────────────────────────────────
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// ── RESPONSE interceptor — gère l'expiration du token (401 STRICT) ───────────
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status

    // STRICT : uniquement HTTP 401 — jamais sur 422 (validation), 500, 502 (Gemini)
    // Évite les faux positifs qui déconnectent l'user sur erreur Gemini ou MongoDB
    if (status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.dispatchEvent(new CustomEvent('auth:expired'))
    }

    return Promise.reject(error)
  }
)

// Auth
export const registerUser = (data)  => api.post('/register', data)
export const loginUser    = (data)  => api.post('/login',    data)
export const getMe        = ()      => api.get('/me')

// Tasks (protégées JWT)
export const getTasks   = ()          => api.get('/tasks/')
export const updateTask = (id, data)  => api.put(`/tasks/${id}`, data)
export const deleteTask = (id)        => api.delete(`/tasks/${id}`)

// Chat AI (protégée JWT)
export const sendChat = (message) => api.post('/chat/', { message })

export default api
