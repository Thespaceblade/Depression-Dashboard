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
import { fetchUpcomingEvents } from '@/src/api/client';
import type { UpcomingEvent, UpcomingEventsData } from '@/src/api/types';
import { colors } from '@/src/theme/colors';
import { typography } from '@/src/theme/typography';

export default function EventsScreen() {
  const [data, setData] = useState<UpcomingEventsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function load() {
    try {
      setError(null);
      const result = await fetchUpcomingEvents();
      setData(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load events');
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
        data={data?.events ?? []}
        keyExtractor={(item, index) => `${item.date}-${item.team}-${index}`}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        contentContainerStyle={styles.listContent}
        renderItem={({ item }) => <EventItem event={item} />}
      />
    </View>
  );
}

function EventItem({ event }: { event: UpcomingEvent }) {
  const date = new Date(event.datetime ?? event.date);

  return (
    <Card style={styles.card}>
      <RNView style={styles.rowHeader}>
        <TeamAvatar name={event.team} sport={event.sport} size={28} />
        <RNView style={styles.rowTitleWrapper}>
          <Text style={styles.cardHeader} numberOfLines={1}>
            {event.team}
          </Text>
          <Text style={styles.vsText} numberOfLines={1}>
            vs <Text style={styles.opponent}>{event.opponent}</Text>
          </Text>
        </RNView>
      </RNView>

      <RNView style={styles.metaRow}>
        <Text style={styles.metaDate}>
          {date.toLocaleDateString()}{' '}
          {date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </Text>
        <Text style={styles.metaType}>{event.type}</Text>
      </RNView>

      <RNView style={styles.tagsRow}>
        <Tag variant={event.is_home ? 'success' : 'warning'}>
          {event.is_home ? 'HOME' : 'AWAY'}
        </Tag>
        <Tag variant="info">{event.sport}</Tag>
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
    gap: 8,
    marginBottom: 4,
  },
  rowTitleWrapper: {
    flex: 1,
  },
  cardHeader: {
    ...typography.body,
    fontWeight: '600',
    color: colors.textPrimary,
  },
  subHeader: {
    fontSize: 13,
    opacity: 0.8,
    marginTop: 2,
  },
  vsText: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  opponent: {
    color: colors.accentBlue,
    fontWeight: '600',
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
  metaType: {
    ...typography.caption,
    color: colors.textSecondary,
  },
  tagsRow: {
    flexDirection: 'row',
    gap: 6,
    marginTop: 8,
  },
  errorText: {
    ...typography.body,
    color: colors.danger,
  },
});



