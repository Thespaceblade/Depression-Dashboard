import { useState } from 'react';
import type { Team } from '../types';
import { getTeamLogo } from '../utils/teamIcons';
import { getDepressionIcon } from '../utils/icons';

interface Props {
  team: Team;
  activityLabel?: string;
}

const getTeamColor = (teamName: string, sport: string): string => {
  const name = teamName.toLowerCase();
  if (name.includes('cowboys')) return 'border-cowboys-blue';
  if (name.includes('mavericks')) return 'border-mavericks-blue';
  if (name.includes('warriors')) return 'border-warriors-blue';
  if (name.includes('rangers')) return 'border-rangers-blue';
  if (name.includes('verstappen') || sport === 'F1') return 'border-f1-red';
  if (sport === 'Fantasy') return 'border-fantasy-purple';
  return 'border-gray-600';
};

const getResultColor = (result: string): string => {
  if (result === 'W' || result === 'P1') return 'bg-green-500';
  if (result === 'L' || result === 'DNF') return 'bg-red-500';
  if (result.startsWith('P')) return 'bg-yellow-500';
  return 'bg-gray-500';
};

export default function TeamCard({ team, activityLabel }: Props) {
  const [expanded, setExpanded] = useState(false);
  const borderColor = getTeamColor(team.name, team.sport);
  const teamLogo = getTeamLogo(team.name, team.sport);
  const moodIcon = getDepressionIcon('', team.depression_points ?? 0, {
    size: 48,
    className: '',
    uniqueKey: team.name, // Use team name as unique key for consistent image selection
  });

  return (
    <div
      className={`bg-card-bg rounded-2xl p-6 border-2 ${borderColor} shadow-xl card-hover cursor-pointer transition-all duration-300`}
      onClick={() => setExpanded(!expanded)}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          {/* Team Logo */}
          <div className="w-12 h-12 flex items-center justify-center flex-shrink-0">
            {teamLogo}
          </div>
          <div>
            <h3 className="text-xl font-bold text-white">{team.name}</h3>
            <p className="text-sm text-gray-400">{team.sport}</p>
          </div>
        </div>
        <div className="text-right flex flex-col items-end gap-2">
          <div className="w-12 h-12 flex items-center justify-center">
            {moodIcon}
          </div>
        </div>
      </div>

      {/* Record */}
      <div className="mb-4">
        {activityLabel && (
          <p className="text-xs text-gray-500 mb-2">Last activity: {activityLabel}</p>
        )}
        <div className="text-3xl font-bold text-white mb-1">
          {team.record}
        </div>
        <div className="flex items-center gap-2">
          <div className="flex-1 bg-gray-700 rounded-full h-2 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-green-500 transition-all duration-500"
              style={{ width: `${team.win_percentage}%` }}
            />
          </div>
          <span className="text-sm text-gray-400 min-w-[50px] text-right">
            {team.win_percentage.toFixed(1)}%
          </span>
        </div>
      </div>

      {/* Recent Streak */}
      {team.recent_streak && team.recent_streak.length > 0 && (
        <div className="mb-4">
          <p className="text-xs text-gray-500 mb-2">Recent Form</p>
          <div className="flex gap-2">
            {team.recent_streak.slice(0, 5).map((result, idx) => (
              <div
                key={idx}
                className={`w-8 h-8 rounded-full ${getResultColor(result)} flex items-center justify-center text-white text-xs font-bold`}
                title={result}
              >
                {result === 'W' ? 'W' : result === 'L' ? 'L' : result === 'DNF' ? 'DNF' : result}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Expandable Details */}
      {expanded && (
        <div className="mt-4 pt-4 border-t border-gray-700 animate-slide-up">
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm text-gray-400 pb-2">
              <span className="text-white font-semibold">Depression Points</span>
              <span className={`font-bold ${(team.depression_points ?? 0) >= 0 ? 'text-red-400' : 'text-green-400'}`}>
                {(team.depression_points ?? 0) >= 0 ? '+' : ''}{(team.depression_points ?? 0).toFixed(1)} pts
              </span>
            </div>
            <div className="text-sm text-gray-400">
              <strong className="text-white">Expected Performance:</strong> {team.expected_performance || 'N/A'}/10
            </div>
            {team.jasons_expectations && (
              <div className="text-sm text-gray-400">
                <strong className="text-white">Jason's Expectations:</strong> {team.jasons_expectations}/10
              </div>
            )}
            {team.championship_position && (
              <div className="text-sm text-gray-400">
                <strong className="text-white">Championship Position:</strong> P{team.championship_position}
              </div>
            )}
            {team.recent_dnfs !== undefined && team.recent_dnfs > 0 && (
              <div className="text-sm text-red-400">
                <strong>Recent DNFs:</strong> {team.recent_dnfs}
              </div>
            )}
            {Object.keys(team.breakdown).length > 0 && (
              <div className="mt-3">
                <p className="text-xs text-gray-500 mb-2">Breakdown:</p>
                {Object.entries(team.breakdown).map(([key, value]) => (
                  <div key={key} className="flex justify-between text-xs text-gray-400 mb-1">
                    <span>{key}:</span>
                    <span className={value >= 0 ? 'text-red-400' : 'text-green-400'}>
                      {value >= 0 ? '+' : ''}{value.toFixed(1)}
                    </span>
                  </div>
                ))}
              </div>
            )}
            {team.notes && (
              <div className="text-xs text-gray-500 italic mt-2">{team.notes}</div>
            )}
          </div>
        </div>
      )}

      {/* Click hint */}
      <div className="text-xs text-gray-600 text-center mt-2">
        {expanded ? 'Click to collapse' : 'Click for details'}
      </div>
    </div>
  );
}
