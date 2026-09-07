/**
 * Maps a depression score (0-100) to an RGB color along win → led → loss.
 */
export function scoreToColor(score: number): string {
  const t = Math.max(0, Math.min(100, score)) / 100;
  // 0 → win green, mid → amber LED, 100 → loss red
  let r: number;
  let g: number;
  let b: number;
  if (t < 0.5) {
    const u = t / 0.5;
    r = Math.round(61 + (255 - 61) * u);
    g = Math.round(220 + (176 - 220) * u);
    b = Math.round(132 + (0 - 132) * u);
  } else {
    const u = (t - 0.5) / 0.5;
    r = Math.round(255 + (255 - 255) * u);
    g = Math.round(176 + (59 - 176) * u);
    b = Math.round(0 + (48 - 0) * u);
  }
  return `rgb(${r}, ${g}, ${b})`;
}

/**
 * Maps depression points to a border color (positive = worse / loss tint).
 */
export function pointsToBorderColor(points: number): string {
  const maxPositive = 50;
  const maxNegative = -50;
  let normalizedScore: number;

  if (points >= 0) {
    normalizedScore = 50 + (Math.min(points, maxPositive) / maxPositive) * 50;
  } else {
    normalizedScore = 50 + (Math.max(points, maxNegative) / Math.abs(maxNegative)) * 50;
  }

  return scoreToColor(normalizedScore);
}
