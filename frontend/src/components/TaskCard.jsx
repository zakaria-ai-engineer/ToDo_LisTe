import { motion, AnimatePresence } from 'framer-motion'
import { Check, Trash2, Calendar, Flag } from 'lucide-react'
import { useState } from 'react'

const P_CONFIG = {
  high:   { color: 'text-red-400',    bg: 'bg-red-500/10',    border: 'border-red-500/30' },
  medium: { color: 'text-yellow-400', bg: 'bg-yellow-500/10', border: 'border-yellow-500/30' },
  low:    { color: 'text-green-400',  bg: 'bg-green-500/10',  border: 'border-green-500/30' },
}

export default function TaskCard({ task, toggleDone, changePriority, removeTask, index }) {
  const [deleting, setDeleting] = useState(false)
  const c = P_CONFIG[task.priority] || P_CONFIG.medium

  const doDelete = async () => {
    setDeleting(true)
    await removeTask(task._id)
  }

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9, transition: { duration: 0.2 } }}
      transition={{ duration: 0.3, delay: index * 0.05 }}
      className={`group relative glass-dark rounded-2xl p-4 flex gap-4 items-start transition-all duration-300 hover:shadow-xl hover:shadow-violet-500/5 hover:-translate-y-1 ${
        task.done ? 'opacity-50 grayscale-[50%]' : ''
      }`}
    >
      {/* Checkbox */}
      <button
        onClick={() => toggleDone(task._id, task.done)}
        className={`mt-1 w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0 transition-all duration-300 ${
          task.done
            ? 'bg-violet-500 border-violet-500 scale-110 shadow-[0_0_15px_rgba(139,92,246,0.5)]'
            : 'border-slate-500 hover:border-violet-400 hover:bg-violet-500/10'
        }`}
      >
        <AnimatePresence>
          {task.done && (
            <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} exit={{ scale: 0 }}>
              <Check size={14} strokeWidth={3} className="text-white" />
            </motion.div>
          )}
        </AnimatePresence>
      </button>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <h3 className={`text-base font-medium transition-colors ${task.done ? 'line-through text-slate-500' : 'text-slate-200'}`}>
          {task.title}
        </h3>
        
        <div className="flex flex-wrap items-center gap-2 mt-3">
          <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-semibold border ${c.bg} ${c.color} ${c.border}`}>
            <Flag size={12} strokeWidth={3} /> {task.priority.toUpperCase()}
          </span>
          
          {task.deadline && (
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium bg-slate-800/80 border border-slate-700 text-slate-400">
              <Calendar size={12} /> {task.deadline}
            </span>
          )}

          {/* Quick Priority Switch (Hover only) */}
          <div className="opacity-0 group-hover:opacity-100 transition-opacity flex items-center gap-1 ml-auto">
            {['low', 'medium', 'high'].map(p => (
              <button key={p} onClick={() => changePriority(task._id, p)}
                className={`w-6 h-6 rounded flex items-center justify-center transition-all ${
                  task.priority === p ? 'bg-slate-700 text-white cursor-default' : 'text-slate-500 hover:bg-slate-800 hover:text-slate-300'
                }`}>
                <Flag size={12} className={p==='high'?'text-red-400':p==='low'?'text-green-400':'text-yellow-400'} />
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Delete Button */}
      <button
        onClick={doDelete} disabled={deleting}
        className="opacity-0 group-hover:opacity-100 absolute top-4 right-4 w-8 h-8 rounded-lg bg-red-500/10 border border-red-500/20 flex items-center justify-center text-red-400 hover:bg-red-500 hover:text-white transition-all transform hover:scale-110 active:scale-95"
      >
        <Trash2 size={14} />
      </button>
    </motion.div>
  )
}
