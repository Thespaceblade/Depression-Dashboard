import { useEffect, useState } from 'react';
import { ActivityIndicator, ScrollView, StyleSheet } from 'react-native';

import { Text, View } from '@/components/Themed';
import { Card } from '@/src/components/Card';
import { SectionHeader } from '@/src/components/SectionHeader';
import { TeamAvatar } from '@/src/components/TeamAvatar';
import { fetchDepression } from '@/src/api/client';
import type { DepressionData } from '@/src/api/types';
import { colors } from '@/src/theme/colors';
import { typography } from '@/src/theme/typography';

export default function HealthScreen() {
  const [data, setData] = useState<DepressionData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      setError(null);
      const result = await fetchDepression();
      setData(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load health data');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  if (loading && !data) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator color={colors.accentBlue} />
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      {error && (
        <Card>
          <SectionHeader>Error</SectionHeader>
          <Text style={styles.errorText}>{error}</Text>
        </Card>
      )}

      {data && (
        <Card>
          <SectionHeader>Depression Breakdown</SectionHeader>
          {Object.entries(data.breakdown)
            .sort(([, a], [, b]) => (b.score || 0) - (a.score || 0))
            .map(([key, value]) => (
              <View key={key} style={styles.breakdownBlock}>
                <View style={styles.breakdownHeader}>
                  <TeamAvatar name={key} size={32} />
                  <View style={styles.breakdownHeaderText}>
                    <Text style={styles.breakdownTitle} numberOfLines={1}>
                      {key}
                    </Text>
                    <Text style={styles.breakdownScore}>
                      Score: {value.score.toFixed(1)}
                    </Text>
                  </View>
                </View>
                {value.details && (
                  <View style={styles.detailList}>
                    {Object.entries(value.details).map(([label, score]) => (
                      <View key={label} style={styles.detailRow}>
                        <Text style={styles.detailLabel}>{label}</Text>
                        <Text style={styles.detailScore}>{score.toFixed(1)}</Text>
                      </View>
                    ))}
                  </View>
                )}
                {value.record && (
                  <Text style={styles.meta}>Record: {value.record}</Text>
                )}
                {value.position && (
                  <Text style={styles.meta}>Position: {value.position}</Text>
                )}
              </View>
            ))}
        </Card>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  centered: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.background,
  },
  container: {
    padding: 16,
    gap: 16,
    backgroundColor: colors.background,
  },
  title: {
    ...typography.titleL,
    color: colors.textPrimary,
    marginBottom: 12,
  },
  breakdownBlock: {
    paddingVertical: 8,
    borderBottomWidth: StyleSheet.hairlineWidth,
    borderBottomColor: 'rgba(148, 163, 184, 0.5)',
  },
  breakdownHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 10,
  },
  breakdownHeaderText: {
    flex: 1,
  },
  breakdownTitle: {
    ...typography.body,
    fontWeight: '600',
    color: colors.textPrimary,
  },
  breakdownScore: {
    marginTop: 4,
    ...typography.body,
    color: colors.danger,
  },
  detailList: {
    marginTop: 6,
    gap: 4,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  detailLabel: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  detailScore: {
    ...typography.caption,
    fontWeight: '600',
    color: colors.textPrimary,
  },
  meta: {
    marginTop: 4,
    ...typography.caption,
    color: colors.textMuted,
  },
  errorText: {
    ...typography.body,
    color: colors.danger,
  },
});



