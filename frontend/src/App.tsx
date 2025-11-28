import { useState, useEffect } from 'react';
import Header from './components/Header';
import DepressionScoreCard from './components/DepressionScoreCard';
import SportSection from './components/SportSection';
import GameTimeline from './components/GameTimeline';
import DepressionBreakdown from './components/DepressionBreakdown';
import UpcomingEvents from './components/UpcomingEvents';
import { fetchDepression, fetchTeams, fetchRecentGames, fetchUpcomingEvents } from './api';
import type { DepressionData, TeamsData, RecentGamesData, UpcomingEventsData, Team } from './types';
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

  // Group teams by sport
  const groupTeamsBySport = (teams: Team[]): Record<string, Team[]> => {
    return teams.reduce((acc, team) => {
      const sport = team.sport;
      if (!acc[sport]) {
        acc[sport] = [];
      }
      acc[sport].push(team);
      return acc;
    }, {} as Record<string, Team[]>);
  };

  if (loading && !depressionData) {
    return (
      <div className="min-h-screen bg-dark-bg flex items-center justify-center">
        <div className="text-center">
          <div className="mb-4 flex justify-center">
            <LoadingIcon size={64} />
          </div>
          <div className="text-2xl text-white font-semibold">Loading depression data...</div>
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

  const teamsBySport = teamsData ? groupTeamsBySport(teamsData.teams) : {};
  // Define order - group NCAA sports together
  const sportOrder = ['NFL', 'NBA', 'MLB', 'NCAA Basketball', 'NCAA Football', 'F1', 'Fantasy'];

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

        {/* Team Performance by Sport */}
        {teamsData && teamsData.teams.length > 0 && (
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-white mb-6">Team Performance by Sport</h2>
            
            {/* Render sport sections in defined order */}
            {sportOrder.map((sport) => {
              if (teamsBySport[sport] && teamsBySport[sport].length > 0) {
                return (
                  <SportSection
                    key={sport}
                    sport={sport}
                    teams={teamsBySport[sport]}
                  />
                );
              }
              return null;
            })}
            
            {/* Render any other sports not in the order list */}
            {Object.entries(teamsBySport).map(([sport, teams]) => {
              if (!sportOrder.includes(sport)) {
                return (
                  <SportSection
                    key={sport}
                    sport={sport}
                    teams={teams}
                  />
                );
              }
              return null;
            })}
          </div>
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
    </div>
  );
}

export default App;
