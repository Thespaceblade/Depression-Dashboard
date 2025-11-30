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
    <header className="bg-card-bg border-b-2 border-gray-700 p-3 sm:p-4 mb-6 sm:mb-8">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-0">
        <div className="flex items-center gap-2 sm:gap-3">
          <img 
            src="/logo.svg" 
            alt="Depression Calculator Logo" 
            className="w-8 h-8 sm:w-10 sm:h-10"
          />
          <div>
            <h1 className="text-xl sm:text-2xl font-bold text-white">Depression Dashboard</h1>
            <p className="text-xs sm:text-sm text-gray-400">
              Last Updated: {formatTime(lastUpdated)}
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-2 sm:gap-3 w-full sm:w-auto justify-between sm:justify-end">
          <button
            onClick={handleRefresh}
            disabled={isRefreshing}
            className="px-3 py-1.5 sm:px-4 sm:py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white rounded-lg text-sm sm:text-base font-semibold transition-colors duration-200 flex items-center gap-2"
          >
            <RefreshIcon spinning={isRefreshing} size={18} />
            <span className="hidden sm:inline">{isRefreshing ? 'Refreshing...' : 'Refresh Data'}</span>
            <span className="sm:hidden">{isRefreshing ? '...' : 'Refresh'}</span>
          </button>

          <div className="flex items-center gap-2">
            <a
              href="https://jasonindata.vercel.app"
              target="_blank"
              rel="noopener noreferrer"
              title="Jason Charwin Portfolio"
              className="w-8 h-8 sm:w-10 sm:h-10 rounded-full border-2 border-blue-500 hover:border-blue-300 hover:bg-blue-500/10 flex items-center justify-center transition-all duration-200"
            >
              <div className="w-6 h-6 sm:w-8 sm:h-8 rounded-full overflow-hidden flex items-center justify-center bg-gray-900">
                {portfolioIconBroken ? (
                  <span className="text-gray-200 text-xs sm:text-sm font-semibold">JD</span>
                ) : (
                  <img
                    src="/image.png"
                    alt="Jason in Data"
                    className="w-full h-full object-cover"
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
              className="w-8 h-8 sm:w-10 sm:h-10 rounded-full border border-gray-600 hover:border-blue-500 hover:bg-blue-500/10 flex items-center justify-center transition-all duration-200 text-gray-200"
            >
              <FaGithub size={16} className="sm:w-5 sm:h-5" />
            </a>
          </div>
        </div>
      </div>
    </header>
  );
}
