import { useEffect, useState } from 'react';
import { ErrorIcon } from '../utils/icons';
import { FaGithub, FaExternalLinkAlt, FaLinkedin } from 'react-icons/fa';

interface ErrorFallbackProps {
  error: string;
  onRetry: () => void;
}

export default function ErrorFallback({ error, onRetry }: ErrorFallbackProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Trigger smooth scroll-down animation on mount
    setIsVisible(true);
  }, []);

  const githubUrl = 'https://github.com/Thespaceblade/Depression-Dashboard';
  const portfolioUrl = 'https://jasonindata.vercel.app';
  const linkedinUrl = 'https://www.linkedin.com/in/jasoncharwin';

  // Unified button hover animation class - same for all buttons
  const buttonHoverClass = "group px-6 py-3 text-white rounded-xl font-medium transition-all duration-300 ease-in-out transform hover:scale-105 hover:shadow-lg hover:shadow-blue-500/30 active:scale-95";

  return (
    <div className="min-h-screen bg-dark-bg overflow-hidden relative">
      {/* Smooth vertical scroll-down page transition */}
      <div
        className={`min-h-screen flex items-center justify-center p-4 transition-all duration-1000 ease-[cubic-bezier(0.4,0,0.2,1)] ${
          isVisible
            ? 'translate-y-0 opacity-100'
            : '-translate-y-[100vh] opacity-0'
        }`}
        style={{
          willChange: 'transform, opacity',
        }}
      >
        <div className="text-center max-w-2xl w-full">
          {/* Error Icon with Animation */}
          <div className="mb-6 flex justify-center">
            <div
              className={`w-20 h-20 sm:w-24 sm:h-24 transition-all duration-700 delay-200 ${
                isVisible ? 'scale-100 rotate-0 opacity-100' : 'scale-0 rotate-180 opacity-0'
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
            className={`text-3xl sm:text-4xl font-bold text-white mb-4 transition-all duration-700 delay-300 ${
              isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
            }`}
          >
            Service Unavailable
          </h1>

          {/* Issue Description */}
          <div
            className={`mb-6 transition-all duration-700 delay-400 ${
              isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
            }`}
          >
            <p className="text-gray-300 mb-3 text-base sm:text-lg leading-relaxed">
              The backend service is currently unavailable. This could be due to:
            </p>
            <ul className="text-gray-400 text-sm sm:text-base text-left max-w-md mx-auto space-y-2 mb-4">
              <li>• The API server is temporarily down or restarting</li>
              <li>• Network connectivity issues</li>
              <li>• The service is being updated or maintained</li>
            </ul>
            <p className="text-red-400 text-sm sm:text-base font-mono bg-red-500/10 border border-red-500/30 rounded-lg p-3 inline-block">
              {error}
            </p>
          </div>

          {/* Project Description */}
          <div
            className={`mb-8 transition-all duration-700 delay-500 ${
              isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
            }`}
          >
            <div className="bg-gray-800/50 border border-gray-700 rounded-xl p-6 text-left">
              <h2 className="text-xl font-semibold text-white mb-3">About This Project</h2>
              <p className="text-gray-300 text-sm sm:text-base leading-relaxed mb-3">
                The <strong className="text-white">Depression Dashboard</strong> is a real-time sports analytics application 
                that calculates a "depression level" based on the performance of my favorite sports teams. 
                It tracks wins, losses, streaks, and recent game results across multiple sports (NFL, NBA, MLB, F1, NCAA) 
                to provide a humorous and data-driven perspective on how team performance affects my mood.
              </p>
              <p className="text-gray-400 text-xs sm:text-sm italic">
                Built with React, TypeScript, Python Flask, and deployed on Railway & Vercel.
              </p>
            </div>
          </div>

          {/* Action Buttons */}
          <div
            className={`flex flex-col sm:flex-row gap-4 justify-center mb-8 transition-all duration-700 delay-600 ${
              isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
            }`}
          >
            <button
              onClick={onRetry}
              className={`${buttonHoverClass} bg-blue-600 hover:bg-blue-700`}
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
            className={`border-t border-gray-700 pt-8 transition-all duration-700 delay-700 ${
              isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'
            }`}
          >
            <p className="text-gray-400 mb-4 text-sm sm:text-base">
              While you're here, check out my portfolio and connect with me on LinkedIn:
            </p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              {/* GitHub Link */}
              <a
                href={githubUrl}
                target="_blank"
                rel="noopener noreferrer"
                className={`${buttonHoverClass} bg-gray-800 hover:bg-gray-700`}
              >
                <span className="flex items-center justify-center gap-2">
                  <FaGithub className="w-5 h-5" />
                  GitHub
                  <FaExternalLinkAlt className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                </span>
              </a>

              {/* Portfolio Link */}
              <a
                href={portfolioUrl}
                target="_blank"
                rel="noopener noreferrer"
                className={`${buttonHoverClass} bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700`}
              >
                <span className="flex items-center justify-center gap-2">
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
                  Portfolio
                  <FaExternalLinkAlt className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                </span>
              </a>

              {/* LinkedIn Link */}
              <a
                href={linkedinUrl}
                target="_blank"
                rel="noopener noreferrer"
                className={`${buttonHoverClass} bg-blue-700 hover:bg-blue-800`}
              >
                <span className="flex items-center justify-center gap-2">
                  <FaLinkedin className="w-5 h-5" />
                  LinkedIn
                  <FaExternalLinkAlt className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                </span>
              </a>
            </div>
          </div>

          {/* Footer Note */}
          <p
            className={`mt-8 text-gray-500 text-xs transition-all duration-700 delay-800 ${
              isVisible ? 'opacity-100' : 'opacity-0'
            }`}
          >
            Built by Jason Charwin
          </p>
        </div>
      </div>
    </div>
  );
}

