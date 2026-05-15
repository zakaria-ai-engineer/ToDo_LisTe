import { useState, useCallback } from 'react'
import { getTasks, updateTask, deleteTask, clearTasks } from '../services/api'

export function useTasks() {
  const [tasks,   setTasks]   = useState([])
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)

  const fetchTasks = useCallback(async (params = {}) => {
    setLoading(true); setError(null)
    try {
      const { data } = await getTasks(params)
      setTasks(data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }, [])

  const toggleDone = useCallback(async (id, current) => {
    try {
      await updateTask(id, { done: !current })
      setTasks(prev => prev.map(t => t._id === id ? { ...t, done: !current } : t))
    } catch (e) { setError(e.response?.data?.detail || 'Error updating task') }
  }, [])

  const changePriority = useCallback(async (id, priority) => {
    try {
      await updateTask(id, { priority })
      setTasks(prev => prev.map(t => t._id === id ? { ...t, priority } : t))
    } catch (e) { setError(e.response?.data?.detail || 'Error updating priority') }
  }, [])

  const removeTask = useCallback(async (id) => {
    try {
      await deleteTask(id)
      setTasks(prev => prev.filter(t => t._id !== id))
    } catch (e) { setError(e.response?.data?.detail || 'Error deleting task') }
  }, [])

  const removeAll = useCallback(async () => {
    try { await clearTasks(); setTasks([]) }
    catch (e) { setError(e.response?.data?.detail || 'Error clearing tasks') }
  }, [])

  return { tasks, loading, error, fetchTasks, toggleDone, changePriority, removeTask, removeAll }
}
