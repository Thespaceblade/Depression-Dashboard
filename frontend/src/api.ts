import type { DepressionData, TeamsData, RecentGamesData, UpcomingEventsData } from './types';

// Use environment variable for production, fallback to proxy for development
const API_BASE = import.meta.env.VITE_API_URL 
  ? `${import.meta.env.VITE_API_URL}/api`
  : '/api';

export async function fetchDepression(): Promise<DepressionData> {
  const response = await fetch(`${API_BASE}/depression`);
  if (!response.ok) {
    throw new Error('Failed to fetch depression data');
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

