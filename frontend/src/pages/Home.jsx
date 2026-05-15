import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowRight } from 'lucide-react';

const features = [
  { title: 'Gestion intuitive', desc: 'Ajoutez vos tâches en quelques secondes.' },
  { title: 'Assistant intelligent', desc: 'L\'IA agit sur simple demande en langage naturel.' },
  { title: 'Données sécurisées', desc: 'Vos tâches sont privées et isolées par session.' },
];

const ease = [0.22, 1, 0.36, 1];

export default function Home() {
  return (
    <div className="min-h-[calc(100vh-4rem)] bg-white flex flex-col">

      {/* ── HERO ───────────────────────────────────────────────────────────── */}
      <div className="flex-1 flex flex-col items-center justify-center text-center px-6 py-28">

        {/* Headline — no badge above */}
        <motion.h1
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.55, ease }}
          className="text-5xl md:text-[62px] font-extrabold text-gray-900 tracking-tight leading-[1.06] max-w-xl"
        >
          Todolist{' '}
          <span className="text-red-500">Intelligent</span>
        </motion.h1>

        {/* Subtitle */}
        <motion.p
          initial={{ opacity: 0, y: 14 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.14, ease }}
          className="mt-4 text-base text-gray-400 max-w-sm leading-relaxed"
        >
          Une gestion simple, rapide et intelligente.
        </motion.p>

        {/* CTAs */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.45, delay: 0.24, ease }}
          className="mt-9 flex flex-col sm:flex-row items-center gap-3"
        >
          <Link
            to="/register"
            className="group inline-flex items-center gap-2 bg-red-500 hover:bg-red-600 text-white font-semibold text-sm px-7 py-3 rounded-xl transition-all duration-200 shadow-card hover:shadow-card-hover hover:scale-[1.02]"
          >
            Commencer
            <ArrowRight size={14} className="group-hover:translate-x-0.5 transition-transform" />
          </Link>
          <Link
            to="/about"
            className="inline-flex items-center bg-white hover:bg-gray-50 border border-gray-200 text-gray-500 font-semibold text-sm px-7 py-3 rounded-xl transition-all duration-200"
          >
            En savoir plus
          </Link>
        </motion.div>
      </div>

      {/* ── BRIDGE SECTION ─────────────────────────────────────────────────── */}
      <div className="py-14 px-6 bg-white border-t border-gray-100">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, ease }}
          className="max-w-xl mx-auto text-center"
        >
          <p className="text-xs text-red-400 font-bold tracking-[0.18em] uppercase mb-3">Comment ça marche</p>
          <h2 className="text-xl font-extrabold text-gray-900 tracking-tight mb-3">
            Organisez vos journées intelligemment
          </h2>
          <p className="text-sm text-gray-400 leading-relaxed">
            Une expérience moderne pour gérer vos tâches rapidement et efficacement.
          </p>
        </motion.div>
      </div>

      {/* ── FEATURES ───────────────────────────────────────────────────────── */}
      <div className="bg-gray-50 border-t border-gray-100 py-16 px-6">
        <div className="max-w-3xl mx-auto">
          <div className="grid md:grid-cols-3 gap-4">
            {features.map((f, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 18 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.09, duration: 0.45, ease }}
                className="group bg-white p-6 rounded-2xl border border-gray-100 shadow-card hover:shadow-card-hover hover:-translate-y-1 transition-all duration-300 cursor-default"
              >
                <div className="w-1.5 h-1.5 rounded-full bg-red-300 group-hover:bg-red-500 mb-4 transition-colors duration-200" />
                <h3 className="font-bold text-gray-900 text-sm mb-1.5">{f.title}</h3>
                <p className="text-gray-400 text-sm leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
