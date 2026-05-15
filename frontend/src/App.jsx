import { AuthProvider } from './context/AuthContext'
import AppRouter from './router/AppRouter'
import './index.css'

export default function App() {
  return (
    <AuthProvider>
      <AppRouter />
    </AuthProvider>
  )
}
