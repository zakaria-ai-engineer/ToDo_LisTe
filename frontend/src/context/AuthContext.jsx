import { createContext, useContext, useState, useCallback, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { loginUser, registerUser } from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    try {
      const stored = localStorage.getItem('user')
      return stored ? JSON.parse(stored) : null
    } catch { return null }
  })

  // useNavigate n'est disponible qu'à l'intérieur d'un Router → ref pour l'accès différé
  const navigateRef = useRef(null)

  // ── Déconnexion (appelée manuellement ou par l'événement global) ────────────
  const logout = useCallback((redirect = true) => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setUser(null)
    if (redirect && navigateRef.current) {
      navigateRef.current('/login', { replace: true })
    }
  }, [])

  // ── Écoute l'événement global émis par l'interceptor axios ─────────────────
  useEffect(() => {
    const handleExpired = () => logout(true)
    window.addEventListener('auth:expired', handleExpired)
    return () => window.removeEventListener('auth:expired', handleExpired)
  }, [logout])

  // ── Login ───────────────────────────────────────────────────────────────────
  const login = useCallback(async (email, password) => {
    const res = await loginUser({ email, password })
    const { access_token, username } = res.data
    localStorage.setItem('token', access_token)
    const u = { username, email }
    localStorage.setItem('user', JSON.stringify(u))
    setUser(u)
    return res.data
  }, [])

  // ── Register ────────────────────────────────────────────────────────────────
  const register = useCallback(async (email, username, password) => {
    const res = await registerUser({ email, username, password })
    const { access_token } = res.data
    localStorage.setItem('token', access_token)
    const u = { username, email }
    localStorage.setItem('user', JSON.stringify(u))
    setUser(u)
    return res.data
  }, [])

  return (
    <AuthContext.Provider value={{ user, login, register, logout, navigateRef }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>')
  return ctx
}
