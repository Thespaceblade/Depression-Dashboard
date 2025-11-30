import { useState } from 'react';
import type { DepressionData } from '../types';
import { getDepressionIcon } from '../utils/icons';
import { scoreToColor } from '../utils/colors';

interface Props {
  data: DepressionData;
}

const getGradientClass = (score: number): string => {
  // Updated to match 10-point ranges (0 = least depressed, 100 = most depressed)
  if (score < 10) return 'from-green-500 to-emerald-600';        // Elated (0-9)
  if (score < 20) return 'from-green-400 to-green-600';          // Thrilled (10-19)
  if (score < 30) return 'from-yellow-400 to-green-500';         // Happy (20-29)
  if (score < 40) return 'from-yellow-500 to-yellow-600';        // Content (30-39)
  if (score < 50) return 'from-gray-400 to-gray-600';            // Neutral (40-49)
  if (score < 60) return 'from-orange-400 to-yellow-500';        // Disappointed (50-59)
  if (score < 70) return 'from-orange-500 to-red-500';           // Sad (60-69)
  if (score < 80) return 'from-red-500 to-red-700';              // Depressed (70-79)
  if (score < 90) return 'from-red-700 to-red-900';              // Miserable (80-89)
  return 'from-red-900 to-red-950';                              // Devastated (90-100)
};

const getProgressPercentage = (score: number): number => {
  // Cap at 100 for visual purposes
  return Math.min((score / 100) * 100, 100);
};

export default function DepressionScoreCard({ data }: Props) {
  const [showInfo, setShowInfo] = useState(false);
  const gradientClass = getGradientClass(data.score);
  const progressPercent = getProgressPercentage(data.score);

  // Get top 3 contributors
  const topContributors = Object.entries(data.breakdown)
    .sort(([, a], [, b]) => (b.score || 0) - (a.score || 0))
    .slice(0, 3)
    .map(([name, data]) => ({ name, score: data.score || 0 }));

  const hoverColor = scoreToColor(data.score);

  return (
    <>
      <div 
        className={`relative overflow-hidden rounded-3xl bg-gradient-to-br ${gradientClass} p-8 shadow-2xl mb-8 animate-fade-in transition-all duration-300 group`}
      >
        {/* Hover overlay */}
        <div
          className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-3xl"
          style={{ backgroundColor: hoverColor }}
        />
        <div className="relative z-10 text-center">
          {/* Large Icon */}
          <div className="flex justify-center mb-4">
            {getDepressionIcon(data.level, data.score)}
          </div>
          
          {/* Score with Info Icon */}
          <div className="flex items-center justify-center gap-4 mb-2">
            <div className="text-7xl font-bold text-white drop-shadow-lg">
              {data.score.toFixed(1)}
            </div>
            <button
              onClick={() => setShowInfo(true)}
              className="flex items-center justify-center w-14 h-14 rounded-full bg-white bg-opacity-30 hover:bg-opacity-50 transition-all duration-200 cursor-pointer group shadow-lg border-2 border-white border-opacity-40 hover:border-opacity-60"
              aria-label="Learn more about the depression score"
            >
              <svg
                className="w-8 h-8 text-white"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={3}
                  d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </button>
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

      {/* Info Modal */}
      {showInfo && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50 backdrop-blur-sm"
          onClick={() => setShowInfo(false)}
        >
          <div
            className="bg-gray-900 rounded-2xl p-8 max-w-lg w-full shadow-2xl border border-gray-700"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start justify-between mb-6">
              <h3 className="text-2xl font-bold text-white">About the Depression Score</h3>
              <button
                onClick={() => setShowInfo(false)}
                className="text-gray-400 hover:text-white transition-colors"
                aria-label="Close"
              >
                <svg
                  className="w-6 h-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>
            
            <div className="space-y-4 text-gray-300">
              <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <p className="text-lg font-semibold text-white mb-2">What does this number mean?</p>
                <p className="text-base leading-relaxed">
                  The depression score measures how Jason's teams' recent performance is affecting Jason's mood. 
                  A lower score (0-10) means Jason's feeling elated, while higher scores indicate increasing levels of 
                  sports-related disappointment. The score ranges from 0 (Elated - least depressed) to 100 (Devastated - most depressed).
                  Each 10-point range represents a different emotional state, from Elated to Devastated.
                </p>
              </div>
              
              <div className="bg-gray-800 rounded-lg p-4 border border-gray-700">
                <p className="text-lg font-semibold text-white mb-2">How it works</p>
                <p className="text-base leading-relaxed">
                  The score is calculated by analyzing recent games, losses, and team performance across all of Jason's 
                  teams. Each loss adds points based on factors like how much Jason expected from the team, 
                  whether Jason's team lost to a rival, if it was a blowout, and how recent the game was. Recent events 
                  have more impact than older ones, with games from the past few days weighted more heavily. 
                  The system also considers expectation gaps. If a team Jason expected to be great is performing poorly, 
                  that hurts more than a bad team losing. Wins can reduce the score, especially unexpected victories. 
                  The final score combines all these factors to give a real-time measure of Jason's sports-related 
                  emotional state.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
