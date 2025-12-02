/**
 * Maps a depression score (0-100) to an RGB color
 * 0 = green (best mood), 100 = red (worst mood)
 */
export function scoreToColor(score: number): string {
  // Clamp score between 0 and 100
  const clampedScore = Math.max(0, Math.min(100, score));
  
  // Calculate RGB values
  // At score 0: green (0, 255, 0)
  // At score 100: red (255, 0, 0)
  const red = Math.round((clampedScore / 100) * 255);
  const green = Math.round(((100 - clampedScore) / 100) * 255);
  const blue = 0;
  
  return `rgb(${red}, ${green}, ${blue})`;
}

/**
 * Maps depression points to a color between red and green
 * Positive values = red (bad impact), negative values = green (good impact)
 * The intensity is based on the absolute value
 */
export function pointsToBorderColor(points: number): string {
  // Define reasonable bounds for depression points
  // Adjust these based on actual data ranges if needed
  const maxPositive = 50;  // Maximum positive depression points
  const maxNegative = -50; // Maximum negative depression points
  
  // Normalize points to 0-100 scale for color calculation
  let normalizedScore: number;
  
  if (points >= 0) {
    // Positive points: map 0 to maxPositive -> score 50 to 100
    normalizedScore = 50 + (Math.min(points, maxPositive) / maxPositive) * 50;
  } else {
    // Negative points: map maxNegative to 0 -> score 0 to 50
    normalizedScore = 50 + (Math.max(points, maxNegative) / Math.abs(maxNegative)) * 50;
  }
  
  return scoreToColor(normalizedScore);
}



