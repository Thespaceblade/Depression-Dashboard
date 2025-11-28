import {
  HiFaceSmile,
  HiFaceFrown,
  HiExclamationTriangle,
  HiXCircle,
  HiCheckCircle,
  HiArrowPath,
  HiChartBar,
  HiCalendarDays,
  HiExclamationCircle,
} from 'react-icons/hi2';
import { 
  MdSportsFootball,
  MdSportsBasketball,
  MdSportsBaseball,
  MdDirectionsCar,
  MdSportsEsports,
} from 'react-icons/md';

// Depression level icons
export const getDepressionIcon = (_level: string, score: number) => {
  const size = 120;
  const className = "animate-pulse-slow";
  
  if (score <= 10) {
    return <HiFaceSmile className={`${className} text-green-400`} style={{ width: size, height: size }} />;
  } else if (score <= 25) {
    return <HiFaceSmile className={`${className} text-yellow-400`} style={{ width: size, height: size }} />;
  } else if (score <= 50) {
    return <HiFaceFrown className={`${className} text-orange-400`} style={{ width: size, height: size }} />;
  } else if (score <= 75) {
    return <HiFaceFrown className={`${className} text-red-400`} style={{ width: size, height: size }} />;
  } else if (score <= 100) {
    return <HiExclamationTriangle className={`${className} text-red-600`} style={{ width: size, height: size }} />;
  } else {
    return <HiXCircle className={`${className} text-gray-400`} style={{ width: size, height: size }} />;
  }
};

// Sport icons
export const getSportIcon = (sport: string, size: number = 24) => {
  const iconProps = { size, className: "text-gray-300" };
  
  switch (sport.toUpperCase()) {
    case 'NFL':
      return <MdSportsFootball {...iconProps} />;
    case 'NBA':
      return <MdSportsBasketball {...iconProps} />;
    case 'MLB':
      return <MdSportsBaseball {...iconProps} />;
    case 'F1':
      return <MdDirectionsCar {...iconProps} />;
    case 'FANTASY':
      return <MdSportsEsports {...iconProps} />;
    default:
      return <HiChartBar {...iconProps} />;
  }
};

// Game result icons
export const getResultIcon = (result: string, size: number = 16) => {
  if (result === 'W' || result === 'P1') {
    return <HiCheckCircle className="text-green-400" style={{ width: size, height: size }} />;
  } else if (result === 'L' || result === 'DNF') {
    return <HiXCircle className="text-red-400" style={{ width: size, height: size }} />;
  } else if (result.startsWith('P')) {
    return <HiExclamationCircle className="text-yellow-400" style={{ width: size, height: size }} />;
  } else {
    return <div className="w-4 h-4 rounded-full bg-gray-500" />;
  }
};

// Loading icon
export const LoadingIcon = ({ size = 64 }: { size?: number }) => (
  <HiFaceFrown className="animate-pulse text-gray-400" style={{ width: size, height: size }} />
);

// Error icon
export const ErrorIcon = ({ size = 64 }: { size?: number }) => (
  <HiXCircle className="text-red-500" style={{ width: size, height: size }} />
);

// Refresh icon
export const RefreshIcon = ({ spinning = false, size = 20 }: { spinning?: boolean; size?: number }) => (
  <HiArrowPath 
    className={spinning ? "animate-spin" : ""} 
    style={{ width: size, height: size }} 
  />
);

// Header icon
export const HeaderIcon = ({ size = 32 }: { size?: number }) => (
  <MdSportsFootball className="text-blue-400" style={{ width: size, height: size }} />
);

// Section header icons
export const ChartIcon = ({ size = 24 }: { size?: number }) => (
  <HiChartBar className="text-blue-400" style={{ width: size, height: size }} />
);

export const CalendarIconComponent = ({ size = 24 }: { size?: number }) => (
  <HiCalendarDays className="text-blue-400" style={{ width: size, height: size }} />
);

