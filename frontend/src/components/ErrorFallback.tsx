import { useEffect, useState } from 'react';
import { ErrorIcon } from '../utils/icons';
import { FaGithub, FaExternalLinkAlt } from 'react-icons/fa';

interface ErrorFallbackProps {
  error: string;
  onRetry: () => void;
}

export default function ErrorFallback({ error, onRetry }: ErrorFallbackProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Trigger animation on mount
    setIsVisible(true);
  }, []);

  const githubUrl = 'https://github.com/Thespaceblade/Depression-Dashboard';
  const portfolioUrl = 'https://jasonindata.vercel.app';

  return (
    <div className="min-h-screen bg-dark-bg flex items-center justify-center p-4">
      <div
        className={`text-center max-w-lg w-full transition-all duration-700 ease-out ${
          isVisible
            ? 'opacity-100 translate-y-0'
            : 'opacity-0 translate-y-8'
        }`}
      >
        {/* Error Icon with Animation */}
        <div className="mb-6 flex justify-center">
          <div
            className={`w-20 h-20 sm:w-24 sm:h-24 transition-all duration-500 delay-100 ${
              isVisible ? 'scale-100 rotate-0' : 'scale-0 rotate-180'
            }`}
          >
            <div className="relative">
              <ErrorIcon size={96} />
              <div className="absolute inset-0 bg-red-500/20 rounded-full blur-xl animate-pulse" />
            </div>
          </div>
        </div>

        {/* Error Title */}
        <h1
          className={`text-3xl sm:text-4xl font-bold text-white mb-3 transition-all duration-500 delay-200 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          }`}
        >
          Service Unavailable
        </h1>

        {/* Error Description */}
        <p
          className={`text-gray-300 mb-2 text-base sm:text-lg transition-all duration-500 delay-300 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          }`}
        >
          The backend service is currently unavailable.
        </p>
        <p
          className={`text-red-400 mb-8 text-sm sm:text-base font-mono transition-all duration-500 delay-400 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          }`}
        >
          {error}
        </p>

        {/* Action Buttons */}
        <div
          className={`flex flex-col sm:flex-row gap-4 justify-center mb-8 transition-all duration-500 delay-500 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          }`}
        >
          <button
            onClick={onRetry}
            className="group px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-semibold transition-all duration-300 transform hover:scale-105 hover:shadow-lg hover:shadow-blue-500/50 active:scale-95"
          >
            <span className="flex items-center justify-center gap-2">
              <svg
                className="w-5 h-5 transition-transform group-hover:rotate-180"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                />
              </svg>
              Try Again
            </span>
          </button>
        </div>

        {/* Links Section */}
        <div
          className={`border-t border-gray-700 pt-8 transition-all duration-500 delay-600 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
          }`}
        >
          <p className="text-gray-400 mb-4 text-sm">Explore more:</p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            {/* GitHub Link */}
            <a
              href={githubUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="group relative px-6 py-3 bg-gray-800 hover:bg-gray-700 text-white rounded-xl font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg hover:shadow-gray-900/50 active:scale-95 overflow-hidden"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-blue-600/0 via-blue-600/20 to-blue-600/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />
              <span className="relative flex items-center justify-center gap-2">
                <FaGithub className="w-5 h-5" />
                View on GitHub
                <FaExternalLinkAlt className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
              </span>
            </a>

            {/* Portfolio Link */}
            <a
              href={portfolioUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="group relative px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-xl font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg hover:shadow-blue-500/50 active:scale-95 overflow-hidden"
            >
              <div className="absolute inset-0 bg-white/10 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
              <span className="relative flex items-center justify-center gap-2">
                <svg
                  className="w-5 h-5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
                My Portfolio
                <FaExternalLinkAlt className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
              </span>
            </a>
          </div>
        </div>

        {/* Footer Note */}
        <p
          className={`mt-8 text-gray-500 text-xs transition-all duration-500 delay-700 ${
            isVisible ? 'opacity-100' : 'opacity-0'
          }`}
        >
          Built by Jason Charwin
        </p>
      </div>
    </div>
  );
}

