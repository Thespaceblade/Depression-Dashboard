import type { DepressionData } from '../types';
import { getDepressionIcon } from '../utils/icons';

interface Props {
  data: DepressionData;
}

const getGradientClass = (score: number): string => {
  if (score <= 10) return 'from-green-500 to-emerald-600';
  if (score <= 25) return 'from-yellow-500 to-orange-500';
  if (score <= 50) return 'from-orange-500 to-red-500';
  if (score <= 75) return 'from-red-600 to-red-800';
  if (score <= 100) return 'from-red-900 to-red-950';
  return 'from-gray-900 to-black';
};

const getProgressPercentage = (score: number): number => {
  // Cap at 100 for visual purposes
  return Math.min((score / 100) * 100, 100);
};

export default function DepressionScoreCard({ data }: Props) {
  const gradientClass = getGradientClass(data.score);
  const progressPercent = getProgressPercentage(data.score);

  // Get top 3 contributors
  const topContributors = Object.entries(data.breakdown)
    .sort(([, a], [, b]) => (b.score || 0) - (a.score || 0))
    .slice(0, 3)
    .map(([name, data]) => ({ name, score: data.score || 0 }));

  return (
    <div className={`relative overflow-hidden rounded-3xl bg-gradient-to-br ${gradientClass} p-8 shadow-2xl mb-8 animate-fade-in`}>
      <div className="relative z-10 text-center">
        {/* Large Icon */}
        <div className="flex justify-center mb-4">
          {getDepressionIcon(data.level, data.score)}
        </div>
        
        {/* Score */}
        <div className="text-7xl font-bold text-white mb-2 drop-shadow-lg">
          {data.score.toFixed(1)}
        </div>
        
        {/* Level */}
        <div className="text-4xl font-semibold text-white mb-6 drop-shadow-md">
          {data.level}
        </div>
        
        {/* Progress Bar */}
        <div className="w-full bg-white bg-opacity-20 rounded-full h-4 mb-6 overflow-hidden">
          <div
            className="h-full bg-white rounded-full transition-all duration-1000 ease-out"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
        
        {/* Breakdown */}
        {topContributors.length > 0 && (
          <div className="flex justify-center gap-4 flex-wrap text-white text-sm">
            <span className="font-semibold">Top Contributors:</span>
            {topContributors.map((contributor, idx) => (
              <span key={idx} className="bg-white bg-opacity-20 px-3 py-1 rounded-full">
                {contributor.name}: {contributor.score.toFixed(1)} pts
              </span>
            ))}
          </div>
        )}
      </div>
      
      {/* Decorative background elements */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-white opacity-5 rounded-full -mr-32 -mt-32" />
      <div className="absolute bottom-0 left-0 w-48 h-48 bg-white opacity-5 rounded-full -ml-24 -mb-24" />
    </div>
  );
}
