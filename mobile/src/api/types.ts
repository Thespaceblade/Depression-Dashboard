export interface Team {
  name: string;
  sport: string;
  wins: number;
  losses: number;
  record: string;
  win_percentage: number;
  recent_streak: string[];
  depression_points: number;
  breakdown: Record<string, number>;
  expected_performance?: number;
  jasons_expectations?: number;
  rivals?: string[];
  recent_rivalry_losses?: string[];
  interest_level?: number;
  notes?: string;
  championship_position?: number;
  recent_dnfs?: number;
}

export interface DepressionData {
  success: boolean;
  score: number;
  level: string;
  emoji: string;
  breakdown: Record<
    string,
    {
      score: number;
      details?: Record<string, number>;
      record?: string;
      position?: string;
    }
  >;
  timestamp: string;
}

export interface TeamsData {
  success: boolean;
  teams: Team[];
  timestamp: string;
}

export interface Game {
  date: string;
  datetime?: string;
  team: string;
  sport: string;
  result: string;
  type: string;
  opponent?: string;
  team_score?: number;
  opponent_score?: number;
  score_margin?: number;
  is_home?: boolean;
  is_overtime?: boolean;
  is_rivalry?: boolean;
}

export interface RecentGamesData {
  success: boolean;
  games: Game[];
  timestamp: string;
}

export interface UpcomingEvent {
  date: string;
  datetime?: string;
  team: string;
  sport: string;
  opponent: string;
  type: string;
  is_home?: boolean;
}

export interface UpcomingEventsData {
  success: boolean;
  events: UpcomingEvent[];
  timestamp: string;
}



