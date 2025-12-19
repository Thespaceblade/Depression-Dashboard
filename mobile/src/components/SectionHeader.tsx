import { PropsWithChildren } from 'react';
import { StyleSheet, View } from 'react-native';

import { Text } from '@/components/Themed';
import { colors } from '../theme/colors';
import { typography } from '../theme/typography';

export function SectionHeader({ children }: PropsWithChildren) {
  return (
    <View style={styles.container}>
      <View style={styles.indicator} />
      <Text style={styles.title}>{children}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  indicator: {
    width: 4,
    height: 20,
    borderRadius: 999,
    backgroundColor: colors.accentBlue,
    marginRight: 8,
  },
  title: {
    ...typography.titleM,
    color: colors.textPrimary,
  },
});




