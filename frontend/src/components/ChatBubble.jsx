export default function ChatBubble({ msg }) {
  const isUser = msg.role === 'user'
  return (
    <div className={`flex items-end gap-2 animate-slide-up ${isUser ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm flex-shrink-0 shadow ${
        isUser
          ? 'bg-gradient-to-br from-indigo-500 to-purple-600'
          : 'bg-slate-700 border border-slate-600'
      }`}>
        {isUser ? '👤' : '🤖'}
      </div>

      {/* Bubble */}
      <div className={`max-w-[78%] px-4 py-3 rounded-2xl text-sm leading-relaxed shadow ${
        isUser
          ? 'bg-gradient-to-br from-indigo-600 to-purple-700 text-white rounded-br-sm'
          : 'bg-slate-800 border border-slate-700 text-slate-200 rounded-bl-sm'
      }`}>
        <p className="whitespace-pre-wrap">{msg.content}</p>
        <p className={`text-[10px] mt-1.5 opacity-40 ${isUser ? 'text-right' : ''}`}>{msg.time}</p>
      </div>
    </div>
  )
}
