import { useState } from 'react';
import type { Team } from '../types';
import TeamCard from './TeamCard';
import { getLeagueLogo } from '../utils/teamIcons';
import { HiChevronDown, HiChevronUp } from 'react-icons/hi2';

interface Props {
  sport: string;
  teams: Team[];
}

export default function SportSection({ sport, teams }: Props) {
  const [isExpanded, setIsExpanded] = useState(true);
  
  if (teams.length === 0) return null;
  
  // Calculate total depression points for this sport
  const totalDepression = teams.reduce((sum, team) => sum + team.depression_points, 0);
  
  return (
    <div className="mb-6">
      {/* Sport Header - Clickable */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full bg-card-bg rounded-xl p-4 border-2 border-gray-700 hover:border-blue-500 transition-all duration-200 flex items-center justify-between mb-4"
      >
        <div className="flex items-center gap-4">
          {/* League Logo */}
          <div className="w-12 h-12 flex items-center justify-center flex-shrink-0">
            {getLeagueLogo(sport)}
          </div>
          
          <div className="text-left">
            <h3 className="text-2xl font-bold text-white">{sport}</h3>
            <p className="text-sm text-gray-400">
              {teams.length} team{teams.length !== 1 ? 's' : ''}
              {totalDepression > 0 && (
                <span className="ml-2 text-red-400">
                  • {totalDepression.toFixed(1)} pts
                </span>
              )}
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          {totalDepression > 0 && (
            <div className="text-right mr-4">
              <div className="text-xl font-bold text-red-400">
                +{totalDepression.toFixed(1)}
              </div>
              <div className="text-xs text-gray-500">total pts</div>
            </div>
          )}
          {isExpanded ? (
            <HiChevronUp className="text-gray-400" size={24} />
          ) : (
            <HiChevronDown className="text-gray-400" size={24} />
          )}
        </div>
      </button>
      
      {/* Teams Grid - Collapsible */}
      {isExpanded && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-slide-up">
          {teams.map((team, idx) => (
            <TeamCard key={idx} team={team} />
          ))}
        </div>
      )}
    </div>
  );
}

