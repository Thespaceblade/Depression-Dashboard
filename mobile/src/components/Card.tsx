import { PropsWithChildren } from 'react';
import { StyleSheet, View, ViewProps } from 'react-native';

import { colors } from '../theme/colors';

interface CardProps extends ViewProps {
  elevated?: boolean;
}

export function Card({ children, style, elevated, ...rest }: PropsWithChildren<CardProps>) {
  return (
    <View
      style={[
        styles.card,
        elevated && styles.cardElevated,
        style,
      ]}
      {...rest}
    >
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    borderRadius: 16,
    padding: 16,
    backgroundColor: colors.cardBackground,
    borderWidth: 1,
    borderColor: colors.cardBorder,
  },
  cardElevated: {
    shadowColor: '#000',
    shadowOpacity: 0.4,
    shadowRadius: 18,
    shadowOffset: { width: 0, height: 10 },
    elevation: 8,
  },
});


