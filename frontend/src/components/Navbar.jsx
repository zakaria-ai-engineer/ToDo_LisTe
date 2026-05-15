import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { motion } from 'framer-motion';
import { CheckCircle, LogOut } from 'lucide-react';

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-sm border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">

          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2 group">
            <motion.div whileHover={{ rotate: 10 }} transition={{ type: 'spring', stiffness: 300 }}>
              <CheckCircle className="h-8 w-8 text-red-500" />
            </motion.div>
            <span className="font-extrabold text-2xl text-red-500 tracking-tight">todo</span>
          </Link>

          {/* Center Links */}
          <div className="hidden md:flex space-x-8">
            {[{ to: '/', label: 'Home' }, { to: '/about', label: 'About Us' }, { to: '/todo', label: 'Todo' }].map(({ to, label }) => (
              <Link
                key={to}
                to={to}
                className="text-gray-600 hover:text-red-500 font-medium transition-colors relative group"
              >
                {label}
                <span className="absolute -bottom-1 left-0 w-0 h-0.5 bg-red-500 group-hover:w-full transition-all duration-300" />
              </Link>
            ))}
          </div>

          {/* Auth Buttons */}
          <div className="flex items-center space-x-3">
            {user ? (
              <>
                <span className="hidden sm:block text-gray-600 text-sm font-medium">
                  👋 {user.username}
                </span>
                <motion.button
                  whileHover={{ scale: 1.03 }}
                  whileTap={{ scale: 0.97 }}
                  onClick={handleLogout}
                  className="flex items-center gap-1.5 bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-full font-medium text-sm transition-colors shadow-sm"
                >
                  <LogOut size={16} />
                  Logout
                </motion.button>
              </>
            ) : (
              <>
                <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}>
                  <Link
                    to="/login"
                    className="bg-red-500 hover:bg-red-600 text-white px-5 py-2 rounded-full font-medium text-sm transition-colors shadow-sm"
                  >
                    SignIn
                  </Link>
                </motion.div>
                <motion.div whileHover={{ scale: 1.03 }} whileTap={{ scale: 0.97 }}>
                  <Link
                    to="/register"
                    className="bg-red-500 hover:bg-red-600 text-white px-5 py-2 rounded-full font-medium text-sm transition-colors shadow-sm"
                  >
                    SignUp
                  </Link>
                </motion.div>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
