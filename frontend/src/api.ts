import type { DepressionData, TeamsData, RecentGamesData, UpcomingEventsData } from './types';

// For Vercel, use relative paths (same domain)
// No need for environment variable since frontend and API are on same domain
const API_BASE = '/api';

export async function fetchDepression(): Promise<DepressionData> {
  const response = await fetch(`${API_BASE}/depression`);
  if (!response.ok) {
    throw new Error('Failed to fetch Jason team data');
  }
  return response.json();
}

export async function fetchTeams(): Promise<TeamsData> {
  const response = await fetch(`${API_BASE}/teams`);
  if (!response.ok) {
    throw new Error('Failed to fetch teams data');
  }
  return response.json();
}

export async function fetchRecentGames(): Promise<RecentGamesData> {
  const response = await fetch(`${API_BASE}/recent-games`);
  if (!response.ok) {
    throw new Error('Failed to fetch recent games');
  }
  return response.json();
}

export async function fetchUpcomingEvents(): Promise<UpcomingEventsData> {
  const response = await fetch(`${API_BASE}/upcoming-events`);
  if (!response.ok) {
    throw new Error('Failed to fetch upcoming events');
  }
  return response.json();
}

export async function refreshData(): Promise<void> {
  const response = await fetch(`${API_BASE}/refresh`, { method: 'POST' });
  if (!response.ok) {
    throw new Error('Failed to refresh data');
  }
}

