/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui'],
        mono: ['JetBrains Mono', 'ui-monospace'],
      },
      colors: {
        violet: {
          950: '#1a0533',
        },
      },
      backgroundImage: {
        'hero-gradient': 'radial-gradient(ellipse 80% 50% at 50% -20%, rgba(120,40,200,0.3), transparent)',
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'glow':  'glow 3s ease-in-out infinite alternate',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%':      { transform: 'translateY(-12px)' },
        },
        glow: {
          from: { boxShadow: '0 0 20px rgba(139,92,246,0.3)' },
          to:   { boxShadow: '0 0 40px rgba(139,92,246,0.7)' },
        },
      },
    },
  },
  plugins: [],
}
