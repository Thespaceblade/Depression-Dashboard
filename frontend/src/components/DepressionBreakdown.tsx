import { useState, useEffect } from 'react';
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';
import type { DepressionData } from '../types';

ChartJS.register(ArcElement, Tooltip, Legend);

interface Props {
  data: DepressionData;
}

const COLORS = [
  '#ff3b30',
  '#ffb000',
  '#3ddc84',
  '#e8e0d0',
  '#c45c26',
  '#7a8f7c',
  '#d4a017',
];

export default function DepressionBreakdown({ data }: Props) {
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => setIsMobile(window.innerWidth < 768);
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const breakdownEntries = Object.entries(data.breakdown || {});

  if (breakdownEntries.length === 0) {
    return (
      <section>
        <h2 className="section-title mb-1">Breakdown</h2>
        <p className="label-caps mb-6">What is moving the score</p>
        <p className="text-muted text-sm">No breakdown data available.</p>
      </section>
    );
  }

  const sortedContributors = breakdownEntries
    .map(([name, entry]) => ({
      name,
      score: entry.score || 0,
      moodImpact: entry.mood_impact ?? Math.abs((entry.score || 0) - 50),
      percentage: 0,
    }))
    .sort((a, b) => b.moodImpact - a.moodImpact);

  const impactTotal = sortedContributors.reduce((sum, c) => sum + c.moodImpact, 0);
  sortedContributors.forEach((c) => {
    c.percentage = impactTotal > 0 ? (c.moodImpact / impactTotal) * 100 : 0;
  });

  const chartData = {
    labels: sortedContributors.map((c) => c.name),
    datasets: [
      {
        data: sortedContributors.map((c) => c.moodImpact),
        backgroundColor: COLORS.slice(0, sortedContributors.length),
        borderColor: '#0c100e',
        borderWidth: 2,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        position: (isMobile ? 'bottom' : 'right') as 'bottom' | 'right',
        labels: {
          color: 'rgba(242, 239, 230, 0.75)',
          font: {
            family: '"IBM Plex Mono", monospace',
            size: isMobile ? 10 : 11,
          },
          boxWidth: 10,
          padding: isMobile ? 8 : 12,
        },
      },
      tooltip: {
        callbacks: {
          label: (context: { label?: string; parsed?: number }) => {
            const label = context.label || '';
            const value = context.parsed || 0;
            const percentage = impactTotal > 0 ? ((value / impactTotal) * 100).toFixed(1) : '0.0';
            return `${label}: ${value.toFixed(1)} impact (${percentage}%)`;
          },
        },
      },
    },
  };

  return (
    <section>
      <h2 className="section-title mb-1">Breakdown</h2>
      <p className="label-caps mb-6">Biggest mood impact first</p>

      <div className="grid md:grid-cols-2 gap-8 items-start border-t border-line pt-6">
        <div className="flex justify-center">
          <div className="w-full max-w-[220px] sm:max-w-[260px]">
            <Doughnut data={chartData} options={options} />
          </div>
        </div>

        <ul className="space-y-4">
          {sortedContributors.map((contributor) => (
            <li key={contributor.name}>
              <div className="flex justify-between gap-3 text-sm mb-1.5">
                <span className="text-ink truncate">{contributor.name}</span>
                <span className="font-mono text-loss flex-shrink-0">
                  {contributor.moodImpact.toFixed(1)}
                </span>
              </div>
              <div className="h-px w-full bg-line overflow-hidden">
                <div
                  className="h-full bg-led transition-all duration-500"
                  style={{ width: `${contributor.percentage}%` }}
                />
              </div>
              <p className="label-caps mt-1 text-right">{contributor.percentage.toFixed(1)}%</p>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
