import { PropsWithChildren } from 'react';
import { StyleSheet, Text, TextProps, View } from 'react-native';

import { colors } from '../theme/colors';

type Variant = 'default' | 'success' | 'danger' | 'warning' | 'info';

interface TagProps extends TextProps {
  variant?: Variant;
}

export function Tag({ children, style, variant = 'default', ...rest }: PropsWithChildren<TagProps>) {
  const bg =
    variant === 'success'
      ? colors.success
      : variant === 'danger'
      ? colors.danger
      : variant === 'warning'
      ? colors.warning
      : variant === 'info'
      ? colors.accentBlue
      : colors.timelineBg;

  return (
    <View style={[styles.container, { backgroundColor: bg }]}>
      <Text style={[styles.text, style]} {...rest}>
        {children}
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 999,
  },
  text: {
    fontSize: 11,
    color: '#fff',
    fontWeight: '600',
  },
});


