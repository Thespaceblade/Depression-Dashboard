import type {
  DepressionData,
  TeamsData,
  RecentGamesData,
  UpcomingEventsData,
} from './types';

// Base URL for the existing backend.
// For development you can point to your local server, and for production
// you can point to your deployed Railway/Render/Vercel backend.
const API_BASE =
  process.env.EXPO_PUBLIC_API_BASE_URL ??
  'https://depression-dashboard-production.up.railway.app';

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

export async function refreshData(): Promise<void> {
  const res = await fetch(`${API_BASE}/api/refresh`, { method: 'POST' });
  await handleResponse<unknown>(res);
}



