// Theme colors that mirror the web dashboard (see frontend/tailwind.config.js)

export const colors = {
  background: '#0f0f1e', // dark-bg
  cardBackground: '#1a1a2e', // card-bg
  cardBorder: '#374151', // approx. gray-700

  textPrimary: '#f9fafb', // gray-50
  textSecondary: '#9ca3af', // gray-400
  textMuted: '#6b7280', // gray-500

  accentBlue: '#3b82f6', // blue-500
  accentPurple: '#6a0dad', // fantasy-purple

  success: '#22c55e', // green-500
  danger: '#ef4444', // red-500
  warning: '#f97316', // orange-500,

  timelineBg: '#1f2937', // gray-800
};

export type ColorKey = keyof typeof colors;

export function getScoreLevelColor(score: number): string {
  if (score < 10) return '#22c55e'; // Elated
  if (score < 20) return '#22c55e'; // Thrilled
  if (score < 30) return '#eab308'; // Happy
  if (score < 40) return '#facc15'; // Content
  if (score < 50) return '#9ca3af'; // Neutral
  if (score < 60) return '#fb923c'; // Disappointed
  if (score < 70) return '#f97316'; // Sad
  if (score < 80) return '#ef4444'; // Depressed
  if (score < 90) return '#b91c1c'; // Miserable
  return '#7f1d1d'; // Devastated
}


