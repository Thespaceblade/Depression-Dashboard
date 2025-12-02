import { useState } from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';

import { colors } from '../theme/colors';

interface TeamAvatarProps {
  name: string;
  sport?: string;
  size?: number;
}

function getInitials(name: string): string {
  const parts = name.split(' ').filter(Boolean);
  if (!parts.length) return '?';
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[1][0]).toUpperCase();
}

function getLogoUrl(name: string, sport?: string): string | null {
  const lower = name.toLowerCase();

  // NFL
  if (sport === 'NFL' || lower.includes('cowboys')) {
    return 'https://a.espncdn.com/i/teamlogos/nfl/500/dal.png';
  }

  // NBA
  if (sport === 'NBA' || lower.includes('mavericks')) {
    return 'https://a.espncdn.com/i/teamlogos/nba/500/dal.png';
  }
  if (lower.includes('warriors') || lower.includes('golden state')) {
    return 'https://a.espncdn.com/i/teamlogos/nba/500/gs.png';
  }

  // MLB
  if (sport === 'MLB' || (lower.includes('rangers') && lower.includes('texas'))) {
    return 'https://a.espncdn.com/i/teamlogos/mlb/500/tex.png';
  }

  // UNC (NCAA)
  if (
    (sport && sport.includes('NCAA')) ||
    lower.includes('north carolina') ||
    lower.includes('tar heels') ||
    lower.includes('unc')
  ) {
    return 'https://a.espncdn.com/i/teamlogos/ncaa/500/153.png';
  }

  // Fantasy
  if (sport === 'Fantasy' || lower.includes('fantasy')) {
    return 'https://a.espncdn.com/i/teamlogos/leagues/500/fantasy.png';
  }

  // F1 / Verstappen – use text avatar instead of logo
  if (sport === 'F1' || lower.includes('verstappen')) {
    return null;
  }

  return null;
}

export function TeamAvatar({ name, sport, size = 32 }: TeamAvatarProps) {
  const [errored, setErrored] = useState(false);
  const initials = getInitials(name);
  const logoUrl = getLogoUrl(name, sport);
  const radius = size / 2;

  // F1 / Verstappen special case
  if (sport === 'F1' || name.toLowerCase().includes('verstappen')) {
    return (
      <View
        style={[
          styles.circle,
          {
            width: size,
            height: size,
            borderRadius: radius,
            backgroundColor: '#dc2626',
          },
        ]}>
        <Text style={styles.text}>MV</Text>
      </View>
    );
  }

  if (logoUrl && !errored) {
    return (
      <Image
        source={{ uri: logoUrl }}
        style={{ width: size, height: size, borderRadius: radius }}
        resizeMode="contain"
        onError={() => setErrored(true)}
      />
    );
  }

  return (
    <View
      style={[
        styles.circle,
        {
          width: size,
          height: size,
          borderRadius: radius,
        },
      ]}>
      <Text style={styles.text}>{initials}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  circle: {
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.timelineBg,
  },
  text: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '700',
  },
});


