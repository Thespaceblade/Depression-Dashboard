import { useState } from 'react';
import { refreshData } from '../api';
import { RefreshIcon } from '../utils/icons';
import { FaGithub } from 'react-icons/fa';

interface Props {
  lastUpdated: string | null;
  onRefresh: () => void;
}

export default function Header({ lastUpdated, onRefresh }: Props) {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [portfolioIconBroken, setPortfolioIconBroken] = useState(false);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      await refreshData();
      onRefresh();
    } catch (error) {
      console.error('Failed to refresh:', error);
    } finally {
      setIsRefreshing(false);
    }
  };

  const formatTime = (timestamp: string | null): string => {
    if (!timestamp) return 'Never';
    try {
      const date = new Date(timestamp);
      return date.toLocaleTimeString();
    } catch {
      return 'Unknown';
    }
  };

  return (
    <header className="bg-card-bg border-b-2 border-gray-700 p-4 mb-8">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <img 
            src="/logo.svg" 
            alt="Depression Calculator Logo" 
            className="w-10 h-10"
          />
          <div>
            <h1 className="text-2xl font-bold text-white">Depression Dashboard</h1>
            <p className="text-sm text-gray-400">
              Last Updated: {formatTime(lastUpdated)}
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <button
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded-lg font-semibold transition-colors duration-200 flex items-center gap-2"
          >
            <RefreshIcon spinning={isRefreshing} size={20} />
            <span>{isRefreshing ? 'Refreshing...' : 'Refresh Data'}</span>
          </button>

          <a
            href="https://jasonindata.vercel.app"
            target="_blank"
            rel="noopener noreferrer"
            title="Jason Charwin Portfolio"
            className="w-10 h-10 rounded-full border-2 border-blue-500 hover:border-blue-300 hover:bg-blue-500/10 flex items-center justify-center transition-all duration-200"
          >
            <div className="w-8 h-8 rounded-full overflow-hidden flex items-center justify-center bg-gray-900">
              {portfolioIconBroken ? (
                <span className="text-gray-200 text-sm font-semibold">JD</span>
              ) : (
                <img
                  src="/image.png"
                  alt="Jason in Data"
                  className="w-12 h-12 object-cover"
                  onError={() => setPortfolioIconBroken(true)}
                />
              )}
            </div>
          </a>
          <a
            href="https://github.com/Thespaceblade/Depression-Dashboard"
            target="_blank"
            rel="noopener noreferrer"
            title="GitHub Repository"
            className="w-10 h-10 rounded-full border border-gray-600 hover:border-blue-500 hover:bg-blue-500/10 flex items-center justify-center transition-all duration-200 text-gray-200"
          >
            <FaGithub />
          </a>
        </div>
      </div>
    </header>
  );
}
