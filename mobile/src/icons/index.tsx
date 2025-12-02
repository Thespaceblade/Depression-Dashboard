import { Ionicons } from '@expo/vector-icons';
import { View } from 'react-native';

import { colors } from '../theme/colors';

export function getSportIcon(sport: string, size: number = 20, color: string = colors.textSecondary) {
  const iconColor = color;
  switch (sport.toUpperCase()) {
    case 'NFL':
      return <Ionicons name="american-football" size={size} color={iconColor} />;
    case 'NBA':
      return <Ionicons name="basketball" size={size} color={iconColor} />;
    case 'MLB':
      return <Ionicons name="baseball" size={size} color={iconColor} />;
    case 'F1':
      return <Ionicons name="car-sport" size={size} color={iconColor} />;
    case 'FANTASY':
      return <Ionicons name="game-controller" size={size} color={iconColor} />;
    default:
      return <Ionicons name="stats-chart" size={size} color={iconColor} />;
  }
}

export function getResultDot(result: string, size: number = 10) {
  let bg = colors.timelineBg;
  if (result === 'W' || result === 'P1') bg = colors.success;
  else if (result === 'L' || result === 'DNF') bg = colors.danger;
  else if (result.startsWith('P')) bg = colors.warning;

  return (
    <View
      style={{
        width: size,
        height: size,
        borderRadius: size / 2,
        backgroundColor: bg,
      }}
    />
  );
}


