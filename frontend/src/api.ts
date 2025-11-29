import type { DepressionData, TeamsData, RecentGamesData, UpcomingEventsData } from './types';

// API base URL - points to Railway backend
// Set VITE_API_URL environment variable in Vercel to your Railway backend URL
// Example: https://depression-dashboard-production.up.railway.app
const API_BASE = import.meta.env.VITE_API_URL || 'https://depression-dashboard-production.up.railway.app';

export async function fetchDepression(): Promise<DepressionData> {
  const response = await fetch(`${API_BASE}/api/depression`);
  if (!response.ok) {
    throw new Error('Failed to fetch Jason team data');
  }
  return response.json();
}

export async function fetchTeams(): Promise<TeamsData> {
  const response = await fetch(`${API_BASE}/api/teams`);
  if (!response.ok) {
    throw new Error('Failed to fetch teams data');
  }
  return response.json();
}

export async function fetchRecentGames(): Promise<RecentGamesData> {
  const response = await fetch(`${API_BASE}/api/recent-games`);
  if (!response.ok) {
    throw new Error('Failed to fetch recent games');
  }
  return response.json();
}

export async function fetchUpcomingEvents(): Promise<UpcomingEventsData> {
  const response = await fetch(`${API_BASE}/api/upcoming-events`);
  if (!response.ok) {
    throw new Error('Failed to fetch upcoming events');
  }
  return response.json();
}

export async function refreshData(): Promise<void> {
  const response = await fetch(`${API_BASE}/api/refresh`, { method: 'POST' });
  if (!response.ok) {
    throw new Error('Failed to refresh data');
  }
}

