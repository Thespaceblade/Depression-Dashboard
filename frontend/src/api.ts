import type { DepressionData, TeamsData, RecentGamesData, UpcomingEventsData } from './types';

/**
 * Prefer same-origin Vercel `/api/*`.
 * Ignore stale VITE_API_URL values that still point at the dead Railway host.
 */
function resolveApiBase(): string {
  const raw = String(import.meta.env.VITE_API_URL ?? '')
    .trim()
    .replace(/\/$/, '');
  if (!raw) return '';
  if (/railway\.app/i.test(raw)) {
    console.warn(
      'Ignoring VITE_API_URL pointing at Railway; using same-origin Vercel APIs.',
    );
    return '';
  }
  return raw;
}

const API_BASE = resolveApiBase();

async function handleApiError(response: Response, action: string): Promise<never> {
  let errorMessage = `Failed to ${action} (${response.status})`;
  if (response.status === 502 || response.status === 503) {
    errorMessage = `API is unavailable (${response.status}). Check the Vercel deployment.`;
  } else {
    try {
      const errorData = await response.json();
      if (errorData.message) {
        errorMessage = `${errorMessage}: ${errorData.message}`;
      }
    } catch {
      // Ignore JSON parse errors
    }
  }
  throw new Error(errorMessage);
}

export async function fetchDepression(): Promise<DepressionData> {
  const response = await fetch(`${API_BASE}/api/depression`);
  if (!response.ok) {
    await handleApiError(response, 'fetch depression data');
  }
  return response.json();
}

export async function fetchTeams(): Promise<TeamsData> {
  const response = await fetch(`${API_BASE}/api/teams`);
  if (!response.ok) {
    await handleApiError(response, 'fetch teams data');
  }
  return response.json();
}

export async function fetchRecentGames(): Promise<RecentGamesData> {
  const response = await fetch(`${API_BASE}/api/recent-games`);
  if (!response.ok) {
    await handleApiError(response, 'fetch recent games');
  }
  return response.json();
}

export async function fetchUpcomingEvents(): Promise<UpcomingEventsData> {
  const response = await fetch(`${API_BASE}/api/upcoming-events`);
  if (!response.ok) {
    await handleApiError(response, 'fetch upcoming events');
  }
  return response.json();
}

export type RefreshResult = {
  success: boolean;
  refreshed: boolean;
  mode?: 'cron_only' | 'live' | string;
  message?: string;
  note?: string;
  timestamp?: string;
};

export async function refreshData(): Promise<RefreshResult> {
  const response = await fetch(`${API_BASE}/api/refresh`, { method: 'POST' });
  if (!response.ok) {
    await handleApiError(response, 'refresh data');
  }
  const data = await response.json();
  return {
    success: Boolean(data.success),
    refreshed: Boolean(data.refreshed),
    mode: data.mode,
    message: data.message,
    note: data.note,
    timestamp: data.timestamp,
  };
}
