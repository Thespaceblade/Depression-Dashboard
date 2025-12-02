import { useEffect, useState } from 'react';
import { ActivityIndicator, RefreshControl, ScrollView, StyleSheet } from 'react-native';

import { Text, View } from '@/components/Themed';
import { Card } from '@/src/components/Card';
import { SectionHeader } from '@/src/components/SectionHeader';
import { TeamAvatar } from '@/src/components/TeamAvatar';
import { colors, getScoreLevelColor } from '@/src/theme/colors';
import { typography } from '@/src/theme/typography';
import { fetchDepression, refreshData } from '@/src/api/client';
import type { DepressionData } from '@/src/api/types';

export default function OverviewScreen() {
  const [data, setData] = useState<DepressionData | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      setError(null);
      const result = await fetchDepression();
      setData(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load data');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  const onRefresh = async () => {
    setRefreshing(true);
    try {
      await refreshData();
    } catch {
      // Ignore refresh errors; we'll still attempt to reload data
    } finally {
      await load();
    }
  };

  if (loading && !data) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator color={colors.accentBlue} />
      </View>
    );
  }

  return (
    <ScrollView
      contentContainerStyle={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}>
      {error && (
        <Card>
          <SectionHeader>Error</SectionHeader>
          <Text style={styles.errorText}>{error}</Text>
        </Card>
      )}

      {data && (
        <>
          <Card elevated>
            <Text style={styles.title}>Overall Depression Score</Text>
            <Text style={styles.score}>
              {data.emoji} {data.score.toFixed(1)}
            </Text>
            <View style={styles.levelRow}>
              <View
                style={[
                  styles.levelPill,
                  { backgroundColor: getScoreLevelColor(data.score) },
                ]}>
                <Text style={styles.levelPillText}>{data.level}</Text>
              </View>
              <Text style={styles.timestamp}>
                Updated {new Date(data.timestamp).toLocaleString()}
              </Text>
            </View>
            <View style={styles.progressTrack}>
              <View
                style={[
                  styles.progressFill,
                  {
                    width: `${Math.min(data.score, 100)}%`,
                    backgroundColor: getScoreLevelColor(data.score),
                  },
                ]}
              />
            </View>
          </Card>

          <Card>
            <SectionHeader>Depression Breakdown</SectionHeader>
            {Object.entries(data.breakdown)
              .sort(([, a], [, b]) => (b.score || 0) - (a.score || 0))
              .map(([key, value]) => (
                <View key={key} style={styles.breakdownRow}>
                  <TeamAvatar name={key} size={32} />
                  <View style={styles.breakdownTextWrapper}>
                    <Text style={styles.breakdownLabel} numberOfLines={1}>
                      {key}
                    </Text>
                    <Text style={styles.breakdownScore}>
                      {value.score.toFixed(1)} pts
                    </Text>
                  </View>
                </View>
              ))}
          </Card>
        </>
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
    marginBottom: 8,
  },
  score: {
    ...typography.metricNumber,
    color: colors.textPrimary,
    marginBottom: 4,
  },
  levelRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginTop: 4,
  },
  levelPill: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 999,
  },
  levelPillText: {
    ...typography.caption,
    color: '#fff',
    fontWeight: '600',
  },
  timestamp: {
    ...typography.caption,
    color: colors.textMuted,
    marginTop: 8,
  },
  progressTrack: {
    marginTop: 12,
    width: '100%',
    height: 8,
    borderRadius: 999,
    backgroundColor: '#111827',
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 999,
  },
  breakdownRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 6,
    gap: 10,
  },
  breakdownTextWrapper: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  breakdownLabel: {
    ...typography.body,
    color: colors.textPrimary,
  },
  breakdownScore: {
    ...typography.body,
    color: colors.danger,
    fontWeight: '600',
  },
  errorText: {
    ...typography.body,
    color: colors.danger,
  },
});



