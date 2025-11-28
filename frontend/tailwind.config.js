/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'dark-bg': '#0f0f1e',
        'card-bg': '#1a1a2e',
        'cowboys-blue': '#003594',
        'cowboys-silver': '#869397',
        'mavericks-blue': '#00538c',
        'warriors-blue': '#1d428a',
        'warriors-gold': '#ffc72c',
        'rangers-blue': '#003278',
        'rangers-red': '#c0111f',
        'f1-red': '#1e41ff',
        'f1-yellow': '#ffeb00',
        'fantasy-purple': '#6a0dad',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.5s ease-in',
        'slide-up': 'slideUp 0.5s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  plugins: [],
}

