const CONFIG = {
  high:   { label: 'HAUTE',   bg: 'bg-red-500/20',    text: 'text-red-400',    dot: 'bg-red-400',    border: 'border-red-500/30'   },
  medium: { label: 'MOYENNE', bg: 'bg-yellow-500/20', text: 'text-yellow-400', dot: 'bg-yellow-400', border: 'border-yellow-500/30' },
  low:    { label: 'BASSE',   bg: 'bg-green-500/20',  text: 'text-green-400',  dot: 'bg-green-400',  border: 'border-green-500/30'  },
}

export default function PriorityBadge({ priority }) {
  const c = CONFIG[priority] ?? CONFIG.medium
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold tracking-widest border ${c.bg} ${c.text} ${c.border}`}>
      <span className={`w-1.5 h-1.5 rounded-full ${c.dot}`} />
      {c.label}
    </span>
  )
}
