import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Trash2, Pencil, CheckCircle2, Circle, X, Check } from 'lucide-react';
import { getTasks, deleteTask, updateTask, sendChat } from '../services/api';

const PRIORITY_STYLES = {
  high: 'bg-red-50 text-red-500 ring-1 ring-red-100',
  medium: 'bg-amber-50 text-amber-600 ring-1 ring-amber-100',
  low: 'bg-green-50 text-green-600 ring-1 ring-green-100',
};

const ease = [0.22, 1, 0.36, 1];

// ── Inline Edit ───────────────────────────────────────────────────────────────
function InlineEdit({ task, onSave, onCancel }) {
  const [val, setVal] = useState(task.title);
  const ref = useRef(null);
  useEffect(() => { ref.current?.focus(); }, []);
  const save = () => {
    const t = val.trim();
    if (t && t !== task.title) onSave(t);
    else onCancel();
  };
  return (
    <div className="flex items-center gap-2 flex-1">
      <input
        ref={ref}
        value={val}
        onChange={e => setVal(e.target.value)}
        onKeyDown={e => { if (e.key === 'Enter') save(); if (e.key === 'Escape') onCancel(); }}
        className="flex-1 text-sm bg-white border border-gray-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-red-400 text-gray-900 shadow-sm"
      />
      <button onClick={save} title="Valider"
        className="p-1.5 rounded-lg bg-green-50 text-green-500 hover:bg-green-100 transition-colors">
        <Check size={12} />
      </button>
      <button onClick={onCancel} title="Annuler"
        className="p-1.5 rounded-lg bg-gray-50 text-gray-400 hover:bg-gray-100 transition-colors">
        <X size={12} />
      </button>
    </div>
  );
}

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [editingId, setEditingId] = useState(null);
  const [messages, setMessages] = useState([{ sender: 'bot', text: 'Bienvenue dans votre espace personnel. Je suis votre assistant intelligent, prêt à vous accompagner dans l\'organisation de votre journée. Que faisons-nous aujourd\'hui ?', fresh: false }]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef(null);

  const fetchTasks = async () => {
    try { const res = await getTasks(); setTasks(res.data); }
    catch (err) { console.error(err); }
  };

  useEffect(() => { fetchTasks(); }, []);
  useEffect(() => { chatEndRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!inputText.trim() || isLoading) return;
    const msg = inputText.trim();
    setMessages(prev => [...prev, { sender: 'user', text: msg, fresh: false }]);
    setInputText('');
    setIsLoading(true);
    try {
      const res = await sendChat(msg);
      setMessages(prev => [...prev, { sender: 'bot', text: res.data.bot_reply, fresh: true }]);
      if (res.data.action !== 'chat') {
        fetchTasks();
      }
    } catch (err) {
      const errMsg = err?.response?.data?.detail || 'عذراً زكرياء، وقع مشكل في الاتصال بالسيرفر.';
      setMessages(prev => [...prev, { sender: 'bot', text: errMsg, isError: true, fresh: false }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleToggleDone = async (task) => {
    try { await updateTask(task._id, { done: !task.done }); fetchTasks(); }
    catch (err) { console.error(err); }
  };

  const handleDelete = async (id) => {
    try { await deleteTask(id); setTasks(prev => prev.filter(t => t._id !== id)); }
    catch (err) { console.error(err); }
  };

  const handleSaveEdit = async (task, newTitle) => {
    try { await updateTask(task._id, { title: newTitle }); setEditingId(null); fetchTasks(); }
    catch (err) { console.error(err); setEditingId(null); }
  };

  const pending = tasks.filter(t => !t.done).length;
  const completed = tasks.filter(t => t.done).length;

  return (
    <div className="h-[calc(100vh-4rem)] flex flex-col md:flex-row gap-8 p-5 md:p-8 max-w-6xl mx-auto w-full">

      {/* ══ CHAT PANEL ════════════════════════════════════════════════════════ */}
      <motion.div
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, ease }}
        className="flex flex-col rounded-2xl overflow-hidden border border-gray-200 shadow-card
                   w-full md:w-[45%] md:shrink-0 h-[52vh] md:h-full"
        style={{ background: 'rgba(255,255,255,0.95)' }}
      >
        {/* ── Chat Header — bg-red-500 matches Logout button exactly */}
        <div className="bg-red-500 px-5 py-4 flex items-center justify-between shrink-0 shadow-sm">
          <div>
            <p className="text-sm font-semibold text-white tracking-tight">Assistant IA</p>
            <p className="text-[11px] text-red-100 mt-0.5">Organisation intelligente</p>
          </div>
          <div className="flex items-center">
            <span className="w-2.5 h-2.5 bg-green-400 rounded-full animate-pulse mr-2" />
            <span className="text-[11px] text-red-100 font-medium">En ligne</span>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto px-4 py-5 space-y-3" style={{ background: 'linear-gradient(180deg, #fffbf8 0%, #ffffff 70%)' }}>
          <AnimatePresence>
            {messages.map((msg, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.2 }}
                className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div className={`max-w-[85%] text-sm leading-relaxed whitespace-pre-wrap px-4 py-2.5 rounded-2xl transition-shadow ${msg.sender === 'user'
                    ? 'bg-red-500 text-white rounded-br-sm shadow-sm'
                    : msg.isError
                      ? 'bg-red-50 text-red-500 border border-red-100 rounded-bl-sm'
                      : `bg-white text-gray-700 border border-gray-100 rounded-bl-sm shadow-sm ${msg.fresh ? 'msg-pulse' : ''}`
                  }`}>
                  {msg.text}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* Typing indicator */}
          {isLoading && (
            <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} className="flex justify-start">
              <div className="bg-white border border-gray-100 shadow-sm rounded-2xl rounded-bl-sm px-4 py-3 flex gap-1.5 items-center">
                <span className="typing-dot" />
                <span className="typing-dot" />
                <span className="typing-dot" />
              </div>
            </motion.div>
          )}
          <div ref={chatEndRef} />
        </div>

        {/* ── Input */}
        <form onSubmit={handleSend} className="px-4 py-3 bg-white/90 border-t border-gray-100 flex gap-2 shrink-0">
          <input
            type="text"
            value={inputText}
            onChange={e => setInputText(e.target.value)}
            disabled={isLoading}
            placeholder="Envoyer un message..."
            className="flex-1 px-4 py-2.5 bg-gray-50/80 border border-gray-200 rounded-xl text-sm text-gray-900 placeholder:text-gray-300 focus:outline-none focus:ring-2 focus:ring-red-300 focus:border-transparent transition-all"
          />
          <motion.button
            whileHover={{ scale: 1.06 }}
            whileTap={{ scale: 0.94 }}
            type="submit"
            disabled={isLoading || !inputText.trim()}
            className="bg-red-500 hover:bg-red-600 text-white w-10 h-10 rounded-xl flex items-center justify-center disabled:opacity-35 transition-colors shrink-0 shadow-sm"
          >
            <Send size={14} />
          </motion.button>
        </form>
      </motion.div>

      {/* ══ TASK PANEL ════════════════════════════════════════════════════════ */}
      <motion.div
        initial={{ opacity: 0, y: 14 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.45, delay: 0.08, ease }}
        className="flex-1 flex flex-col overflow-hidden min-h-0 w-full md:w-[55%]"
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-3.5 shrink-0">
          <h2 className="text-sm font-bold text-gray-900 tracking-tight">Mes Tâches</h2>
          <div className="flex items-center gap-2 text-[11px] font-semibold">
            <span className="bg-gray-100 text-gray-500 px-2.5 py-1 rounded-lg">{pending} à faire</span>
            {completed > 0 && (
              <span className="bg-green-50 text-green-600 px-2.5 py-1 rounded-lg ring-1 ring-green-100">{completed} faites</span>
            )}
          </div>
        </div>

        {/* Task List */}
        <div className="flex-1 overflow-y-auto space-y-3 pb-2 min-h-0">
          {tasks.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.4 }}
              className="flex flex-col items-center justify-center h-full text-center bg-white rounded-2xl border border-gray-100 shadow-sm py-20"
            >
              <div className="w-9 h-9 rounded-xl bg-gray-50 border border-gray-100 flex items-center justify-center mb-3">
                <CheckCircle2 size={18} className="text-gray-200" />
              </div>
              <p className="text-gray-400 text-sm font-medium">Aucune tâche.</p>
              <p className="text-gray-300 text-xs mt-1">Utilisez l'assistant pour commencer.</p>
            </motion.div>
          ) : (
            <AnimatePresence>
              {tasks.map((task) => (
                <motion.div
                  key={task._id}
                  initial={{ opacity: 0, y: 6 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, x: -8, scale: 0.98 }}
                  transition={{ duration: 0.18 }}
                  className={`group bg-white border rounded-xl px-4 py-3 flex items-center gap-3 shadow-sm transition-all duration-200 ${task.done
                      ? 'border-gray-100 opacity-40'
                      : 'border-gray-200 hover:border-gray-300 hover:shadow-card hover:-translate-y-px'
                    }`}
                >
                  {/* Toggle */}
                  <button
                    onClick={() => handleToggleDone(task)}
                    className="shrink-0 text-gray-200 hover:text-red-400 active:scale-90 transition-all"
                  >
                    {task.done
                      ? <CheckCircle2 size={18} className="text-green-400" />
                      : <Circle size={18} />}
                  </button>

                  {/* Content */}
                  {editingId === task._id ? (
                    <InlineEdit task={task} onSave={t => handleSaveEdit(task, t)} onCancel={() => setEditingId(null)} />
                  ) : (
                    <div className="flex-1 min-w-0 flex items-center gap-2">
                      <span className={`text-sm truncate ${task.done ? 'line-through text-gray-300' : 'text-gray-800 font-medium'}`}>
                        {task.title}
                      </span>
                      {task.priority && PRIORITY_STYLES[task.priority] && (
                        <span className={`shrink-0 text-[10px] font-bold px-1.5 py-0.5 rounded-md capitalize ${PRIORITY_STYLES[task.priority]}`}>
                          {task.priority}
                        </span>
                      )}
                    </div>
                  )}

                  {/* Hover actions */}
                  {editingId !== task._id && (
                    <div className="flex items-center gap-0.5 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity duration-150">
                      <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}
                        onClick={() => setEditingId(task._id)}
                        className="p-1.5 rounded-lg text-gray-300 hover:text-gray-600 hover:bg-gray-50 transition-all">
                        <Pencil size={12} />
                      </motion.button>
                      <motion.button whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}
                        onClick={() => handleDelete(task._id)}
                        className="p-1.5 rounded-lg text-gray-300 hover:text-red-500 hover:bg-red-50 transition-all">
                        <Trash2 size={12} />
                      </motion.button>
                    </div>
                  )}
                </motion.div>
              ))}
            </AnimatePresence>
          )}
        </div>
      </motion.div>
    </div>
  );
}
