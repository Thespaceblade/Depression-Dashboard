import { TextStyle } from 'react-native';

export const typography = {
  titleXL: {
    fontSize: 28,
    fontWeight: '700',
  } as TextStyle,
  titleL: {
    fontSize: 22,
    fontWeight: '700',
  } as TextStyle,
  titleM: {
    fontSize: 18,
    fontWeight: '600',
  } as TextStyle,
  body: {
    fontSize: 14,
  } as TextStyle,
  caption: {
    fontSize: 12,
  } as TextStyle,
  metricNumber: {
    fontSize: 32,
    fontWeight: '800',
  } as TextStyle,
};

export type TypographyKey = keyof typeof typography;




