import { useState, useEffect, useMemo } from 'react';
import { Analytics } from '@vercel/analytics/react';
import Header from './components/Header';
import DepressionScoreCard from './components/DepressionScoreCard';
import TeamCard from './components/TeamCard';
import GameTimeline from './components/GameTimeline';
import DepressionBreakdown from './components/DepressionBreakdown';
import UpcomingEvents from './components/UpcomingEvents';
import { fetchDepression, fetchTeams, fetchRecentGames, fetchUpcomingEvents } from './api';
import type { DepressionData, TeamsData, RecentGamesData, UpcomingEventsData } from './types';
import { LoadingIcon, ErrorIcon } from './utils/icons';

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
    
    // Auto-refresh every 60 seconds
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
      if (game.date) {
        labelParts.push(game.date);
      }
      if (game.result && game.result !== '?') {
        labelParts.push(`Result: ${game.result}`);
      }
      if (game.opponent) {
        labelParts.push(`vs ${game.opponent}`);
      }

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
        if (b.order === a.order) {
          return a.fallbackIndex - b.fallbackIndex;
        }
        return b.order - a.order;
      });
  }, [teamsData, activityMap]);

  if (loading && !depressionData) {
    return (
      <div className="min-h-screen bg-dark-bg flex items-center justify-center">
        <div className="text-center">
          <div className="mb-4 flex justify-center">
            <LoadingIcon size={64} />
          </div>
          <div className="text-2xl text-white font-semibold">Loading Jason team data...</div>
          <div className="text-gray-400 mt-2">This might take a moment</div>
        </div>
      </div>
    );
  }

  if (error && !depressionData) {
    return (
      <div className="min-h-screen bg-dark-bg flex items-center justify-center p-4">
        <div className="text-center max-w-md">
          <div className="mb-4 flex justify-center">
            <ErrorIcon size={64} />
          </div>
          <div className="text-2xl text-white font-semibold mb-2">Error Loading Data</div>
          <div className="text-red-400 mb-4">{error}</div>
          <button
            onClick={loadData}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-bg">
      <div className="max-w-7xl mx-auto px-4 py-8">
        <Header
          lastUpdated={depressionData?.timestamp || null}
          onRefresh={loadData}
        />

        {/* Hero Depression Score Card */}
        {depressionData && (
          <DepressionScoreCard data={depressionData} />
        )}

        {/* Team Grid ordered by recent activity */}
        {sortedTeams.length > 0 && (
          <section className="mb-8">
            <div className="flex flex-col md:flex-row md:items-baseline md:justify-between gap-2 mb-6">
              <div>
                <h2 className="text-3xl font-bold text-white">Team Mood Board</h2>
                <p className="text-sm text-gray-400">
                  Most recently active teams float to the top • 3-up grid
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
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

        {/* Recent Games and Breakdown */}
        <div className="grid lg:grid-cols-2 gap-6 mb-8">
          {gamesData && (
            <GameTimeline games={gamesData.games} />
          )}
          
          {depressionData && (
            <DepressionBreakdown data={depressionData} />
          )}
        </div>

        {/* Upcoming Events */}
        {upcomingEventsData && upcomingEventsData.events.length > 0 && (
          <div className="mb-8">
            <UpcomingEvents events={upcomingEventsData.events} />
          </div>
        )}

        {/* Footer */}
        <footer className="text-center text-gray-500 text-sm mt-12 pb-8">
          <p>Depression Dashboard</p>
          <p className="mt-2">
            {depressionData && `Current Score: ${depressionData.score.toFixed(1)} - ${depressionData.level}`}
          </p>
        </footer>
      </div>
      <Analytics />
    </div>
  );
}

export default App;
