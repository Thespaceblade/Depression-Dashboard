import { useState, useEffect } from 'react';
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';
import type { DepressionData } from '../types';
import { ChartIcon } from '../utils/icons';

ChartJS.register(ArcElement, Tooltip, Legend);

interface Props {
  data: DepressionData;
}

export default function DepressionBreakdown({ data }: Props) {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const breakdownEntries = Object.entries(data.breakdown);
  
  if (breakdownEntries.length === 0) {
    return (
      <div className="bg-card-bg rounded-xl sm:rounded-2xl p-4 sm:p-6 border-2 border-gray-700">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-6 h-6 sm:w-7 sm:h-7">
            <ChartIcon size={24} />
          </div>
          <h2 className="text-xl sm:text-2xl font-bold text-white">Depression Breakdown</h2>
        </div>
        <p className="text-gray-400 text-sm sm:text-base">No breakdown data available</p>
      </div>
    );
  }

  // Prepare chart data
  const labels = breakdownEntries.map(([name]) => name);
  const values = breakdownEntries.map(([, data]) => data.score || 0);
  const total = values.reduce((sum, val) => sum + val, 0);

  // Color palette
  const colors = [
    '#ef4444', // red
    '#f97316', // orange
    '#eab308', // yellow
    '#22c55e', // green
    '#3b82f6', // blue
    '#8b5cf6', // purple
    '#ec4899', // pink
  ];

  const chartData = {
    labels,
    datasets: [
      {
        data: values,
        backgroundColor: colors.slice(0, labels.length),
        borderColor: '#1a1a2e',
        borderWidth: 2,
      },
    ],
  };

  const legendPosition: 'bottom' | 'right' = isMobile ? 'bottom' : 'right';
  
  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: legendPosition,
        labels: {
          color: '#e0e0e0',
          font: {
            size: isMobile ? 10 : 12,
          },
          boxWidth: isMobile ? 12 : 15,
          padding: isMobile ? 8 : 12,
        },
      },
      tooltip: {
        callbacks: {
          label: (context: any) => {
            const label = context.label || '';
            const value = context.parsed || 0;
            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : '0.0';
            return `${label}: ${value.toFixed(1)} pts (${percentage}%)`;
          },
        },
      },
    },
  };

  // Top contributors list
  const sortedContributors = breakdownEntries
    .map(([name, data]) => ({
      name,
      score: data.score || 0,
      percentage: total > 0 ? ((data.score || 0) / total) * 100 : 0,
    }))
    .sort((a, b) => b.score - a.score);

  return (
    <div className="bg-card-bg rounded-xl sm:rounded-2xl p-4 sm:p-6 border-2 border-gray-700">
      <div className="flex items-center gap-2 mb-4 sm:mb-6">
        <div className="w-6 h-6 sm:w-7 sm:h-7">
          <ChartIcon size={24} />
        </div>
        <h2 className="text-xl sm:text-2xl font-bold text-white">Depression Breakdown</h2>
      </div>
      
      <div className="grid md:grid-cols-2 gap-4 sm:gap-6">
        {/* Chart */}
        <div className="flex items-center justify-center">
          <div className="w-full max-w-[250px] sm:max-w-xs">
            <Doughnut data={chartData} options={options} />
          </div>
        </div>

        {/* Top Contributors List */}
        <div>
          <h3 className="text-base sm:text-lg font-semibold text-white mb-3 sm:mb-4">Top Contributors</h3>
          <div className="space-y-2 sm:space-y-3">
            {sortedContributors.map((contributor, idx) => (
              <div key={idx} className="space-y-1">
                <div className="flex justify-between items-center gap-2">
                  <span className="text-white font-medium text-sm sm:text-base truncate">{contributor.name}</span>
                  <span className="text-red-400 font-bold text-sm sm:text-base flex-shrink-0">
                    {contributor.score.toFixed(1)} pts
                  </span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-red-500 to-orange-500 transition-all duration-500"
                    style={{ width: `${contributor.percentage}%` }}
                  />
                </div>
                <div className="text-xs text-gray-500 text-right">
                  {contributor.percentage.toFixed(1)}% of total
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
