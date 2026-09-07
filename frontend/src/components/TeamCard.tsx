import { useState } from 'react';
import type { Team } from '../types';
import { getTeamLogo } from '../utils/teamIcons';
import { pointsToBorderColor } from '../utils/colors';

interface Props {
  team: Team;
  activityLabel?: string;
}

const streakTone = (result: string): string => {
  if (result === 'W' || result === 'P1') return 'text-win';
  if (result === 'L' || result === 'DNF') return 'text-loss';
  if (result.startsWith('P')) return 'text-led';
  return 'text-muted';
};

export default function TeamCard({ team, activityLabel }: Props) {
  const [expanded, setExpanded] = useState(false);
  const teamLogo = getTeamLogo(team.name, team.sport);
  const accent = pointsToBorderColor(team.depression_points ?? 0);

  return (
    <article
      className="border-t border-line cursor-pointer transition-colors duration-200 hover:bg-panel/60"
      style={{ borderLeft: `3px solid ${accent}` }}
      onClick={() => setExpanded(!expanded)}
    >
      <div className="px-3 sm:px-4 py-4 sm:py-5 flex items-start gap-3 sm:gap-4">
        <div className="w-10 h-10 sm:w-11 sm:h-11 flex-shrink-0">{teamLogo}</div>

        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-baseline justify-between gap-x-3 gap-y-1">
            <h3 className="font-display text-lg sm:text-xl uppercase tracking-wide text-ink truncate">
              {team.name}
            </h3>
            <p className="font-mono text-xl sm:text-2xl tabular-nums text-ink">{team.record}</p>
          </div>
          <p className="label-caps mt-1">
            {team.sport}
            <span className="mx-2 text-line">/</span>
            {team.win_percentage.toFixed(1)}%
          </p>
          {activityLabel && (
            <p className="mt-2 text-xs text-muted line-clamp-2">{activityLabel}</p>
          )}
          {team.recent_streak && team.recent_streak.length > 0 && (
            <p className="mt-2 font-mono text-sm tracking-[0.2em]">
              {team.recent_streak.slice(0, 5).map((result, idx) => (
                <span key={idx} className={streakTone(result)}>
                  {result}
                  {idx < Math.min(team.recent_streak.length, 5) - 1 ? ' ' : ''}
                </span>
              ))}
            </p>
          )}
        </div>
      </div>

      {expanded && (
        <div className="px-3 sm:px-4 pb-5 pl-[3.25rem] sm:pl-[4.25rem] animate-panel-expand overflow-hidden">
          <div className="space-y-2 text-sm text-muted border-t border-line pt-4">
            <div className="flex justify-between gap-3">
              <span className="label-caps">Depression points</span>
              <span
                className={`font-mono ${(team.depression_points ?? 0) >= 0 ? 'text-loss' : 'text-win'}`}
              >
                {(team.depression_points ?? 0) >= 0 ? '+' : ''}
                {(team.depression_points ?? 0).toFixed(1)}
              </span>
            </div>
            <div className="flex justify-between gap-3">
              <span>Expected</span>
              <span className="font-mono text-ink">{team.expected_performance || 'N/A'}/10</span>
            </div>
            {team.jasons_expectations != null && (
              <div className="flex justify-between gap-3">
                <span>Jason&apos;s expectations</span>
                <span className="font-mono text-ink">{team.jasons_expectations}/10</span>
              </div>
            )}
            {team.championship_position != null && (
              <div className="flex justify-between gap-3">
                <span>Championship</span>
                <span className="font-mono text-ink">P{team.championship_position}</span>
              </div>
            )}
            {team.recent_dnfs != null && team.recent_dnfs > 0 && (
              <div className="flex justify-between gap-3 text-loss">
                <span>Recent DNFs</span>
                <span className="font-mono">{team.recent_dnfs}</span>
              </div>
            )}
            {Object.keys(team.breakdown).length > 0 && (
              <div className="pt-2 space-y-1">
                <p className="label-caps mb-2">Breakdown</p>
                {Object.entries(team.breakdown).map(([key, value]) => (
                  <div key={key} className="flex justify-between gap-3 text-xs">
                    <span className="truncate mr-2">{key}</span>
                    <span className={`font-mono flex-shrink-0 ${value >= 0 ? 'text-loss' : 'text-win'}`}>
                      {value >= 0 ? '+' : ''}
                      {value.toFixed(1)}
                    </span>
                  </div>
                ))}
              </div>
            )}
            {team.notes && <p className="text-xs italic pt-1">{team.notes}</p>}
            <p className="label-caps pt-2">{expanded ? 'Tap to collapse' : 'Tap for details'}</p>
          </div>
        </div>
      )}

      {!expanded && (
        <p className="px-3 sm:px-4 pb-3 pl-[3.25rem] sm:pl-[4.25rem] label-caps">Tap for details</p>
      )}
    </article>
  );
}
