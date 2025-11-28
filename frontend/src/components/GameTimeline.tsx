import type { Game } from '../types';
import { getSportIcon, getResultIcon, CalendarIconComponent } from '../utils/icons';

interface Props {
  games: Game[];
}

const getResultColor = (result: string): string => {
  if (result === 'W' || result === 'P1') return 'bg-green-500';
  if (result === 'L' || result === 'DNF') return 'bg-red-500';
  if (result.startsWith('P')) return 'bg-yellow-500';
  return 'bg-gray-500';
};

export default function GameTimeline({ games }: Props) {
  if (games.length === 0) {
    return (
      <div className="bg-card-bg rounded-2xl p-6 border-2 border-gray-700">
        <div className="flex items-center gap-2 mb-4">
          <CalendarIconComponent size={28} />
          <h2 className="text-2xl font-bold text-white">Recent Games & Events</h2>
        </div>
        <p className="text-gray-400">No recent games to display</p>
      </div>
    );
  }

  return (
    <div className="bg-card-bg rounded-2xl p-6 border-2 border-gray-700">
      <div className="flex items-center gap-2 mb-6">
        <CalendarIconComponent size={28} />
        <h2 className="text-2xl font-bold text-white">Recent Games & Events</h2>
      </div>
      
      <div className="space-y-4">
        {games.slice(0, 10).map((game, idx) => (
          <div
            key={idx}
            className="flex items-start gap-4 p-4 bg-gray-800 bg-opacity-50 rounded-lg hover:bg-opacity-70 transition-all duration-200 animate-fade-in"
            style={{ animationDelay: `${idx * 0.1}s` }}
          >
            {/* Timeline dot */}
            <div className={`w-4 h-4 rounded-full ${getResultColor(game.result)} flex-shrink-0 mt-1`} />
            
            {/* Content */}
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <div className="flex items-center">
                  {getSportIcon(game.sport, 20)}
                </div>
                <span className="font-semibold text-white">{game.team}</span>
                {game.is_rivalry && (
                  <span className="text-xs bg-red-600 text-white px-2 py-1 rounded-full">
                    RIVALRY!
                  </span>
                )}
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-400">
                <div className="flex items-center">
                  {getResultIcon(game.result, 16)}
                </div>
                <span>Result: {game.result}</span>
                <span className="text-gray-600">•</span>
                <span>{game.date}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
