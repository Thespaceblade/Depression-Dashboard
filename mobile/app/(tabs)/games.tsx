import { useEffect, useState } from 'react';
import {
  ActivityIndicator,
  FlatList,
  RefreshControl,
  StyleSheet,
  View as RNView,
} from 'react-native';

import { Text, View } from '@/components/Themed';
import { Card } from '@/src/components/Card';
import { SectionHeader } from '@/src/components/SectionHeader';
import { Tag } from '@/src/components/Tag';
import { TeamAvatar } from '@/src/components/TeamAvatar';
import { fetchRecentGames } from '@/src/api/client';
import type { Game, RecentGamesData } from '@/src/api/types';
import { getResultDot } from '@/src/icons';
import { colors } from '@/src/theme/colors';
import { typography } from '@/src/theme/typography';

export default function GamesScreen() {
  const [data, setData] = useState<RecentGamesData | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      setError(null);
      const result = await fetchRecentGames();
      setData(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load games');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    load();
  };

  if (loading && !data) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator color={colors.accentBlue} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {error && (
        <Card>
          <SectionHeader>Error</SectionHeader>
          <Text style={styles.errorText}>{error}</Text>
        </Card>
      )}
      <FlatList
        data={data?.games ?? []}
        keyExtractor={(item, index) => `${item.date}-${item.team}-${index}`}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        contentContainerStyle={styles.listContent}
        renderItem={({ item }) => <GameItem game={item} />}
      />
    </View>
  );
}

function GameItem({ game }: { game: Game }) {
  const date = new Date(game.datetime ?? game.date);
  const lost = game.result.toLowerCase().startsWith('l');

  return (
    <Card style={styles.card}>
      <RNView style={styles.rowHeader}>
        {getResultDot(game.result, 10)}
        <TeamAvatar name={game.team} sport={game.sport} size={28} />
        <RNView style={styles.rowTitleWrapper}>
          <Text style={styles.cardHeader} numberOfLines={1}>
            {game.team}
          </Text>
          {game.opponent && (
            <Text style={styles.vsText} numberOfLines={1}>
              vs <Text style={styles.opponent}>{game.opponent}</Text>
            </Text>
          )}
        </RNView>
      </RNView>

      <RNView style={styles.metaRow}>
        <Text style={[styles.result, lost && styles.resultLost]}>
          {game.result}{' '}
          {game.team_score != null && game.opponent_score != null
            ? `(${game.team_score}–${game.opponent_score})`
            : ''}
        </Text>
        <Text style={styles.metaDate}>
          {date.toLocaleDateString()}{' '}
          {date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </Text>
      </RNView>

      <RNView style={styles.tagsRow}>
        {game.is_home != null && (
          <Tag variant={game.is_home ? 'success' : 'warning'}>
            {game.is_home ? 'HOME' : 'AWAY'}
          </Tag>
        )}
        {game.is_overtime && <Tag variant="info">OT</Tag>}
        {game.is_rivalry && (
          <Tag variant="danger">
            RIVALRY!
          </Tag>
        )}
        <Tag variant="info">{game.sport}</Tag>
      </RNView>
    </Card>
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
    flex: 1,
    backgroundColor: colors.background,
  },
  listContent: {
    padding: 16,
  },
  card: {
    marginBottom: 12,
    borderLeftWidth: 3,
    borderLeftColor: colors.accentBlue,
  },
  rowHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 6,
    gap: 8,
  },
  rowTitleWrapper: {
    flex: 1,
  },
  cardHeader: {
    ...typography.body,
    fontWeight: '600',
    color: colors.textPrimary,
  },
  vsText: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  opponent: {
    color: colors.accentBlue,
    fontWeight: '600',
  },
  subHeader: {
    fontSize: 13,
    opacity: 0.8,
    marginTop: 2,
  },
  result: {
    ...typography.body,
    fontWeight: '700',
    color: colors.success,
  },
  resultLost: {
    color: colors.danger,
  },
  metaRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 4,
  },
  metaDate: {
    ...typography.caption,
    color: colors.textMuted,
  },
  tagsRow: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 6,
    marginTop: 8,
  },
  errorText: {
    ...typography.body,
    color: colors.danger,
  },
});



