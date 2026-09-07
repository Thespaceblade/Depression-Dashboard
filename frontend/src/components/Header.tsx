import { useState } from 'react';
import { refreshData } from '../api';

interface Props {
  lastUpdated: string | null;
  onRefresh: () => void;
}

export default function Header({ lastUpdated, onRefresh }: Props) {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    setStatusMessage(null);
    try {
      const result = await refreshData();
      onRefresh();

      if (result.refreshed) {
        setStatusMessage(result.message || 'Sports data refreshed.');
      } else {
        setStatusMessage(
          result.message ||
            'Dashboard reloaded. Sports records update on a schedule, not from this button.'
        );
      }
    } catch (error) {
      console.error('Failed to refresh:', error);
      setStatusMessage('Could not reload dashboard data.');
    } finally {
      setIsRefreshing(false);
    }
  };

  const formatTime = (timestamp: string | null): string => {
    if (!timestamp) return 'Never';
    try {
      return new Date(timestamp).toLocaleTimeString();
    } catch {
      return 'Unknown';
    }
  };

  return (
    <header className="border-b border-line">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 py-3 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div className="min-w-0">
          <p className="label-caps">Last updated {formatTime(lastUpdated)}</p>
          {statusMessage && (
            <p className="font-mono text-xs text-led mt-1 max-w-xl">{statusMessage}</p>
          )}
        </div>

        <div className="flex items-center gap-4 sm:gap-5 flex-wrap">
          <button
            type="button"
            onClick={handleRefresh}
            disabled={isRefreshing}
            title="Reload the dashboard. On Vercel, sports source data updates via scheduled cron."
            className="util-btn"
          >
            {isRefreshing ? 'Reloading…' : 'Reload'}
          </button>
          <a
            href="https://jasonindata.vercel.app"
            target="_blank"
            rel="noopener noreferrer"
            className="util-link"
          >
            Portfolio
          </a>
          <a
            href="https://github.com/Thespaceblade/Depression-Dashboard"
            target="_blank"
            rel="noopener noreferrer"
            className="util-link"
          >
            GitHub
          </a>
        </div>
      </div>
    </header>
  );
}
