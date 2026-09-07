import { useState, useEffect, useMemo } from 'react';
import { Analytics } from '@vercel/analytics/react';
import Header from './components/Header';
import DepressionScoreCard from './components/DepressionScoreCard';
import TeamCard from './components/TeamCard';
import GameTimeline from './components/GameTimeline';
import DepressionBreakdown from './components/DepressionBreakdown';
import UpcomingEvents from './components/UpcomingEvents';
import ErrorFallback from './components/ErrorFallback';
import { fetchDepression, fetchTeams, fetchRecentGames, fetchUpcomingEvents } from './api';
import type { DepressionData, TeamsData, RecentGamesData, UpcomingEventsData } from './types';

function App() {
  const [depressionData, setDepressionData] = useState<DepressionData | null>(null);
  const [teamsData, setTeamsData] = useState<TeamsData | null>(null);
  const [gamesData, setGamesData] = useState<RecentGamesData | null>(null);
  const [upcomingEventsData, setUpcomingEventsData] = useState<UpcomingEventsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [depression, teams, games, upcoming] = await Promise.all([
        fetchDepression(),
        fetchTeams(),
        fetchRecentGames(),
        fetchUpcomingEvents(),
      ]);

      setDepressionData(depression);
      setTeamsData(teams);
      setGamesData(games);
      setUpcomingEventsData(upcoming);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 60000);
    return () => clearInterval(interval);
  }, []);

  const teamKey = (name: string, sport: string) =>
    `${name.toLowerCase()}|${sport.toLowerCase()}`;

  const activityMap = useMemo(() => {
    if (!gamesData?.games) return new Map<string, { label: string; order: number }>();

    const map = new Map<string, { label: string; order: number }>();
    const total = gamesData.games.length;

    gamesData.games.forEach((game, index) => {
      const key = teamKey(game.team, game.sport);
      if (map.has(key)) return;

      const labelParts: string[] = [];
      if (game.date) labelParts.push(game.date);
      if (game.result && game.result !== '?') labelParts.push(`Result: ${game.result}`);
      if (game.opponent) labelParts.push(`vs ${game.opponent}`);

      map.set(key, {
        label: labelParts.join(' • ') || 'Recent action logged',
        order: total - index,
      });
    });

    return map;
  }, [gamesData]);

  const sortedTeams = useMemo(() => {
    if (!teamsData?.teams) return [];

    return teamsData.teams
      .map((team, index) => {
        const key = teamKey(team.name, team.sport);
        const activity = activityMap.get(key);

        return {
          team,
          activityLabel: activity?.label,
          order: activity?.order ?? 0,
          fallbackIndex: index,
        };
      })
      .sort((a, b) => {
        if (b.order === a.order) return a.fallbackIndex - b.fallbackIndex;
        return b.order - a.order;
      });
  }, [teamsData, activityMap]);

  if (loading && !depressionData) {
    return (
      <div className="min-h-screen bg-field flex items-center justify-center p-6 animate-flood-in">
        <div className="text-center">
          <p className="font-display text-3xl sm:text-4xl uppercase text-ink tracking-wide mb-3">
            Depression Dashboard
          </p>
          <p className="label-caps text-led">Loading board…</p>
        </div>
      </div>
    );
  }

  if (error && !depressionData) {
    return <ErrorFallback error={error} onRetry={loadData} />;
  }

  return (
    <div className="min-h-screen bg-field text-ink">
      <Header
        lastUpdated={depressionData?.timestamp || null}
        onRefresh={loadData}
      />

      {depressionData && <DepressionScoreCard data={depressionData} />}

      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-16 space-y-16 sm:space-y-20">
        {sortedTeams.length > 0 && (
          <section>
            <h2 className="section-title mb-1">Teams</h2>
            <p className="label-caps mb-6">Most recent activity first</p>
            <div className="border-b border-line">
              {sortedTeams.map(({ team, activityLabel }) => (
                <TeamCard
                  key={`${team.name}-${team.sport}`}
                  team={team}
                  activityLabel={activityLabel}
                />
              ))}
            </div>
          </section>
        )}

        <div className="grid lg:grid-cols-2 gap-12 lg:gap-16">
          {gamesData && <GameTimeline games={gamesData.games} />}
          {depressionData && <DepressionBreakdown data={depressionData} />}
        </div>

        {upcomingEventsData && upcomingEventsData.events.length > 0 && (
          <UpcomingEvents events={upcomingEventsData.events} />
        )}

        <footer className="section-rule pt-8 pb-4 text-center">
          <p className="font-display text-sm uppercase tracking-widest text-muted">
            Depression Dashboard
          </p>
          {depressionData && (
            <p className="font-mono text-xs text-muted mt-2">
              {depressionData.score.toFixed(1)} · {depressionData.level}
            </p>
          )}
        </footer>
      </div>
      <Analytics />
    </div>
  );
}

export default App;
