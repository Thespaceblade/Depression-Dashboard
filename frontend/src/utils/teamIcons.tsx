// Team and League icon mappings
// Using team logos from CDN or inline SVG representations

import { useState } from 'react';

const TeamLogoImage = ({ src, alt, fallback }: { src: string; alt: string; fallback: JSX.Element }) => {
  const [hasError, setHasError] = useState(false);
  
  if (hasError) {
    return fallback;
  }
  
  return (
    <img 
      src={src} 
      alt={alt}
      className="w-full h-full object-contain"
      onError={() => setHasError(true)}
    />
  );
};

export const getTeamLogo = (teamName: string, sport: string): JSX.Element => {
  const name = teamName.toLowerCase();
  const initials = teamName.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
  const fallback = (
    <div className="w-full h-full flex items-center justify-center bg-panel border border-line">
      <span className="text-ink font-mono font-bold text-xs">{initials}</span>
    </div>
  );
  
  // NFL Teams
  if (sport === 'NFL') {
    if (name.includes('cowboys')) {
      return (
        <TeamLogoImage 
          src="https://a.espncdn.com/i/teamlogos/nfl/500/dal.png" 
          alt="Dallas Cowboys"
          fallback={fallback}
        />
      );
    }
  }
  
  // NBA Teams
  if (sport === 'NBA') {
    if (name.includes('mavericks')) {
      return (
        <TeamLogoImage 
          src="https://a.espncdn.com/i/teamlogos/nba/500/dal.png" 
          alt="Dallas Mavericks"
          fallback={fallback}
        />
      );
    }
    if (name.includes('warriors') || name.includes('golden state')) {
      return (
        <TeamLogoImage 
          src="https://a.espncdn.com/i/teamlogos/nba/500/gs.png" 
          alt="Golden State Warriors"
          fallback={fallback}
        />
      );
    }
  }
  
  // MLB Teams
  if (sport === 'MLB') {
    if (name.includes('rangers') && name.includes('texas')) {
      return (
        <TeamLogoImage 
          src="https://a.espncdn.com/i/teamlogos/mlb/500/tex.png" 
          alt="Texas Rangers"
          fallback={fallback}
        />
      );
    }
  }
  
  // NCAA Teams
  if (sport.includes('NCAA')) {
    if (name.includes('north carolina') || name.includes('tar heels') || name.includes('unc')) {
      return (
        <TeamLogoImage 
          src="https://a.espncdn.com/i/teamlogos/ncaa/500/153.png" 
          alt="North Carolina Tar Heels"
          fallback={fallback}
        />
      );
    }
  }
  
  // F1
  if (sport === 'F1' || name.includes('verstappen')) {
    return (
      <TeamLogoImage 
        src="/maxverstappen.jpeg" 
        alt="Max Verstappen"
        fallback={
          <div className="w-full h-full flex items-center justify-center bg-f1-red">
            <span className="text-ink font-mono font-bold text-xs">MV</span>
          </div>
        }
      />
    );
  }
  
  // Fantasy Teams
  if (sport === 'Fantasy') {
    // Check for Jason's Supreme Team specifically
    if (name.includes("supreme") || name.includes("jason's")) {
      return (
        <TeamLogoImage 
          src="https://a.espncdn.com/i/teamlogos/leagues/500/fantasy.png" 
          alt="ESPN Fantasy"
          fallback={
            <div className="w-full h-full flex items-center justify-center bg-led">
              <span className="text-field font-mono font-bold text-xs">ESPN</span>
            </div>
          }
        />
      );
    }
    return (
      <div className="w-full h-full flex items-center justify-center bg-panel border border-led">
        <span className="text-led font-mono font-bold text-xs">FF</span>
      </div>
    );
  }
  
  // Default fallback
  return fallback;
};

// League logo SVGs as inline components
const NFLLogo = () => (
  <svg viewBox="0 0 100 100" className="w-full h-full">
    <rect width="100" height="100" rx="8" fill="#013369"/>
    <text x="50" y="60" fontSize="40" fontWeight="bold" fill="white" textAnchor="middle" fontFamily="Arial, sans-serif">NFL</text>
  </svg>
);

const NBALogo = () => (
  <svg viewBox="0 0 100 100" className="w-full h-full">
    <rect width="100" height="100" rx="8" fill="#C8102E"/>
    <text x="50" y="60" fontSize="40" fontWeight="bold" fill="white" textAnchor="middle" fontFamily="Arial, sans-serif">NBA</text>
  </svg>
);

const MLBLogo = () => (
  <svg viewBox="0 0 100 100" className="w-full h-full">
    <rect width="100" height="100" rx="8" fill="#132448"/>
    <text x="50" y="60" fontSize="40" fontWeight="bold" fill="white" textAnchor="middle" fontFamily="Arial, sans-serif">MLB</text>
  </svg>
);

const NCAALogo = () => (
  <svg viewBox="0 0 100 100" className="w-full h-full">
    <rect width="100" height="100" rx="8" fill="#003366"/>
    <text x="50" y="60" fontSize="32" fontWeight="bold" fill="white" textAnchor="middle" fontFamily="Arial, sans-serif">NCAA</text>
  </svg>
);

// ESPN Fantasy Logo
const ESPNFantasyLogo = () => (
  <svg viewBox="0 0 100 100" className="w-full h-full">
    <rect width="100" height="100" fill="#141a15" stroke="#ffb000" strokeWidth="3"/>
    <text x="50" y="45" fontSize="18" fontWeight="bold" fill="#ffb000" textAnchor="middle" fontFamily="IBM Plex Mono, monospace">ESPN</text>
    <text x="50" y="70" fontSize="16" fontWeight="bold" fill="#f2efe6" textAnchor="middle" fontFamily="IBM Plex Mono, monospace">FANTASY</text>
  </svg>
);

export const getLeagueLogo = (sport: string): JSX.Element => {
  const sportUpper = sport.toUpperCase();
  const fallback = (
    <div className="w-full h-full flex items-center justify-center bg-gray-700 rounded">
      <span className="text-white font-bold text-sm">{sportUpper}</span>
    </div>
  );
  
  // Handle NCAA sports
  if (sportUpper.includes('NCAA')) {
    return <NCAALogo />;
  }
  
  switch (sportUpper) {
    case 'NFL':
      return <NFLLogo />;
    case 'NBA':
      return <NBALogo />;
    case 'MLB':
      return <MLBLogo />;
    case 'F1':
      return (
        <div className="w-full h-full flex items-center justify-center bg-red-600 rounded">
          <span className="text-white font-bold text-sm">F1</span>
        </div>
      );
    case 'FANTASY':
      return <ESPNFantasyLogo />;
    default:
      return fallback;
  }
};

