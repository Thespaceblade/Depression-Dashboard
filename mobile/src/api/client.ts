import type {
  DepressionData,
  TeamsData,
  RecentGamesData,
  UpcomingEventsData,
} from './types';

// Base URL for the Vercel serverless API.
// Override with EXPO_PUBLIC_API_BASE_URL for local/dev backends.
const API_BASE =
  process.env.EXPO_PUBLIC_API_BASE_URL ??
  'https://depression-dashboard.vercel.app';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const message = await response.text().catch(() => '');
    throw new Error(
      `API error ${response.status}: ${response.statusText} ${message}`.trim(),
    );
  }
  return response.json() as Promise<T>;
}

export async function fetchDepression(): Promise<DepressionData> {
  const res = await fetch(`${API_BASE}/api/depression`);
  return handleResponse<DepressionData>(res);
}

export async function fetchTeams(): Promise<TeamsData> {
  const res = await fetch(`${API_BASE}/api/teams`);
  return handleResponse<TeamsData>(res);
}

export async function fetchRecentGames(): Promise<RecentGamesData> {
  const res = await fetch(`${API_BASE}/api/recent-games`);
  return handleResponse<RecentGamesData>(res);
}

export async function fetchUpcomingEvents(): Promise<UpcomingEventsData> {
  const res = await fetch(`${API_BASE}/api/upcoming-events`);
  return handleResponse<UpcomingEventsData>(res);
}

export type RefreshResult = {
  success: boolean;
  refreshed: boolean;
  mode?: string;
  message?: string;
};

export async function refreshData(): Promise<RefreshResult> {
  const res = await fetch(`${API_BASE}/api/refresh`, { method: 'POST' });
  const data = await handleResponse<RefreshResult & Record<string, unknown>>(res);
  return {
    success: Boolean(data.success),
    refreshed: Boolean(data.refreshed),
    mode: typeof data.mode === 'string' ? data.mode : undefined,
    message: typeof data.message === 'string' ? data.message : undefined,
  };
}





