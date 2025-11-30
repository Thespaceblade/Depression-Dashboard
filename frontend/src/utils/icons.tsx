import { useState, useEffect, useMemo } from 'react';
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

interface DepressionIconOptions {
  size?: number;
  className?: string;
}

// Map of folder numbers to available image filenames
const EMOTIONAL_STATE_IMAGES: Record<number, string[]> = {
  1: ['IMG_9402.JPG', 'IMG_9683.JPG'],
  2: ['2.PNG', '2.jpg', '22.jpeg'],
  3: ['3.jpg', '33.jpg', 'IMG_9665.JPG', 'IMG_9691.JPG'],
  4: ['4.jpg', '44.jpg', '444.jpg', 'IMG_9578.JPG'],
  5: ['5.jpg', 'IMG_9402.JPG'],
  6: ['6.jpg', 'IMG_0894.jpg', 'IMG_0895.jpg', 'IMG_9480.JPG'],
  7: ['7.jpg', 'IMG_0893.jpg', 'IMG_9698.JPG'],
  8: ['88.jpg', 'IMG_8470.jpeg', 'IMG_9629.JPG'],
  9: ['9.jpg', '99.JPG', 'IMG_9448.JPG'],
  10: ['10.JPG', 'IMG_0892.jpg', 'IMG_9397.JPG'],
};

// Map depression score to folder number (1-10)
// Score is now 0-100 scale where 0 = best, 100 = worst
// Folder 1 = worst (high scores 80-100), Folder 10 = best (low scores 0-20)
const getFolderNumberFromScore = (score: number): number => {
  // High scores (bad) → lower folders (1-5)
  // Medium scores (neutral) → middle folders (5-7)
  // Low scores (good) → higher folders (8-10)
  
  // Clamp score to 0-100 range
  const clampedScore = Math.max(0, Math.min(100, score));
  
  if (clampedScore >= 80) return 1;      // Very high depression (worst) - 80-100
  if (clampedScore >= 70) return 2;     // High depression - 70-79
  if (clampedScore >= 60) return 3;      // Pretty depressed - 60-69
  if (clampedScore >= 50) return 4;      // Moderately depressed - 50-59
  if (clampedScore >= 40) return 5;      // Somewhat depressed - 40-49
  if (clampedScore >= 30) return 6;      // Mildly disappointed - 30-39
  if (clampedScore >= 20) return 7;      // Slightly disappointed - 20-29
  if (clampedScore >= 10) return 8;      // Doing okay - 10-19
  if (clampedScore > 0) return 9;        // Feeling good - 1-9
  return 10;                              // Feeling great! (best) - 0
};

// Simple hash function to create a seed from a string
const hashString = (str: string): number => {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32bit integer
  }
  return Math.abs(hash);
};

// Component for displaying emotional state images
const EmotionalStateImage = ({ 
  score, 
  size = 120, 
  className = '',
  uniqueKey = '' 
}: { 
  score: number; 
  size?: number; 
  className?: string;
  uniqueKey?: string;
}) => {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [imageError, setImageError] = useState(false);

  // Get folder number for this score
  const folderNum = useMemo(() => getFolderNumberFromScore(score), [score]);

  useEffect(() => {
    const availableImages = EMOTIONAL_STATE_IMAGES[folderNum] || [];
    
    if (availableImages.length > 0) {
      // Create a seed using both score and uniqueKey to ensure different images for different teams
      // even if they have the same score
      const seedValue = uniqueKey 
        ? hashString(uniqueKey + score.toString())
        : Math.floor(score * 1000 + Math.random() * 1000);
      const seed = seedValue % availableImages.length;
      const imagePath = `/emotional states/${folderNum}/${availableImages[seed]}`.replace(/ /g, '%20');
      setSelectedImage(imagePath);
      setImageError(false);
    } else {
      setSelectedImage(null);
    }
  }, [folderNum, score, uniqueKey]); // Change when folder number, score, or unique key changes

  // Fallback to icon if image fails or folder is empty
  if (!selectedImage || imageError) {
    const baseClass = className || 'animate-pulse-slow';
    // Score is 0-100 where 0 = best, 100 = worst
    const clampedScore = Math.max(0, Math.min(100, score));
    if (clampedScore <= 10) {
      return <HiFaceSmile className={`${baseClass} text-green-400`} style={{ width: size, height: size }} />;
    } else if (clampedScore <= 25) {
      return <HiFaceSmile className={`${baseClass} text-yellow-400`} style={{ width: size, height: size }} />;
    } else if (clampedScore <= 50) {
      return <HiFaceFrown className={`${baseClass} text-orange-400`} style={{ width: size, height: size }} />;
    } else if (clampedScore <= 75) {
      return <HiFaceFrown className={`${baseClass} text-red-400`} style={{ width: size, height: size }} />;
    } else {
      return <HiExclamationTriangle className={`${baseClass} text-red-600`} style={{ width: size, height: size }} />;
    }
  }

  return (
    <div 
      className={`relative inline-block rounded-2xl overflow-hidden shadow-2xl transition-all duration-300 hover:scale-110 hover:shadow-[0_20px_40px_rgba(0,0,0,0.5)] hover:rotate-2 cursor-pointer ${className}`}
      style={{ 
        width: size, 
        height: size,
      }}
    >
      <img
        src={selectedImage}
        alt={`Emotional state for score ${score}`}
        className="w-full h-full object-cover"
        style={{
          objectPosition: 'center',
          aspectRatio: '1 / 1',
        }}
        onError={() => setImageError(true)}
      />
      <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
    </div>
  );
};

// Depression level icons - now uses emotional state images
export const getDepressionIcon = (
  _level: string,
  score: number,
  options?: DepressionIconOptions & { uniqueKey?: string },
) => {
  const size = options?.size ?? 120;
  const baseClass = options?.className ?? '';
  const uniqueKey = options?.uniqueKey ?? '';

  return (
    <EmotionalStateImage 
      score={score} 
      size={size} 
      className={baseClass}
      uniqueKey={uniqueKey}
    />
  );
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

