import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { ArrowRight } from 'lucide-react';

const ease = [0.22, 1, 0.36, 1];

export default function About() {
  return (
    <div className="min-h-[calc(100vh-4rem)] bg-white flex flex-col">

      {/* ── SPLIT HERO ─────────────────────────────────────────────────────── */}
      <section className="flex flex-col md:flex-row flex-1 min-h-[480px]">

        {/* Left — Cinematic image */}
        <motion.div
          initial={{ opacity: 0, x: -28 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.7, ease }}
          className="md:w-1/2 relative min-h-[260px] md:min-h-0 overflow-hidden bg-gray-100"
        >
          <motion.img
            src="https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&w=1200&q=85"
            alt="Organisation de tâches"
            className="absolute inset-0 w-full h-full object-cover"
            initial={{ scale: 1.08 }}
            animate={{ scale: 1 }}
            transition={{ duration: 1.2, ease }}
          />
          {/* Gradient vignette */}
          <div className="absolute inset-0 bg-gradient-to-r from-black/10 via-transparent to-transparent" />
          <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />
        </motion.div>

        {/* Right — Text */}
        <motion.div
          initial={{ opacity: 0, x: 28 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.7, delay: 0.1, ease }}
          className="md:w-1/2 flex flex-col justify-center px-10 md:px-14 lg:px-20 py-16 bg-white"
        >
          <span className="text-red-400 text-[11px] font-bold tracking-[0.18em] uppercase mb-5 block">
            À propos
          </span>

          <h1 className="text-3xl md:text-4xl font-extrabold text-gray-900 tracking-tight leading-tight mb-4">
            About Todo AI
          </h1>

          <p className="text-gray-400 text-base leading-relaxed mb-8 max-w-xs">
            Une plateforme moderne pour organiser vos tâches avec simplicité et intelligence.
          </p>

          <Link
            to="/register"
            className="group inline-flex items-center gap-2 bg-red-500 hover:bg-red-600 text-white font-semibold text-sm px-6 py-2.5 rounded-xl w-fit transition-all duration-200 hover:scale-[1.02] shadow-card hover:shadow-card-hover"
          >
            Commencer
            <ArrowRight size={14} className="group-hover:translate-x-0.5 transition-transform" />
          </Link>
        </motion.div>
      </section>

      {/* ── STRIP ──────────────────────────────────────────────────────────── */}
      <section className="border-t border-gray-100 bg-gray-50 py-10 px-6">
        <div className="max-w-3xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
          {[
            { label: 'Simple',      desc: 'Prise en main immédiate.' },
            { label: 'Intelligent', desc: 'L\'IA comprend le langage naturel.' },
            { label: 'Sécurisé',   desc: 'Données isolées par session.' },
          ].map((item, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 12 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.08, duration: 0.4, ease }}
            >
              <p className="font-bold text-gray-900 text-sm mb-1">{item.label}</p>
              <p className="text-gray-400 text-sm leading-relaxed">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  );
}
