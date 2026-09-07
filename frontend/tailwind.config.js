/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        field: 'var(--field)',
        flood: 'var(--flood)',
        led: 'var(--led)',
        ink: 'var(--ink)',
        win: 'var(--win)',
        loss: 'var(--loss)',
        panel: 'var(--panel)',
        line: 'var(--line)',
        muted: 'var(--muted)',
        // Keep team accents for thin row rules only
        'cowboys-blue': '#003594',
        'cowboys-silver': '#869397',
        'mavericks-blue': '#00538c',
        'warriors-blue': '#1d428a',
        'warriors-gold': '#ffc72c',
        'rangers-blue': '#003278',
        'rangers-red': '#c0111f',
        'f1-red': '#e10600',
        'f1-yellow': '#ffeb00',
        // Legacy aliases → scoreboard tokens (avoid purple SaaS leftovers)
        'dark-bg': 'var(--field)',
        'card-bg': 'var(--panel)',
      },
      fontFamily: {
        display: ['"Archivo Black"', 'Impact', 'sans-serif'],
        mono: ['"IBM Plex Mono"', 'ui-monospace', 'monospace'],
        sans: ['"IBM Plex Sans"', 'Helvetica', 'Arial', 'sans-serif'],
      },
      animation: {
        'flood-in': 'floodIn 0.9s ease-out forwards',
        'score-tick': 'scoreTick 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) forwards',
        'panel-expand': 'panelExpand 0.25s ease-out forwards',
      },
      keyframes: {
        floodIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        scoreTick: {
          '0%': { opacity: '0', transform: 'translateY(0.4em)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        panelExpand: {
          '0%': { opacity: '0', maxHeight: '0' },
          '100%': { opacity: '1', maxHeight: '40rem' },
        },
      },
    },
  },
  plugins: [],
}
