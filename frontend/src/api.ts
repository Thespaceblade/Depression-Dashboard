import type { DepressionData, TeamsData, RecentGamesData, UpcomingEventsData } from './types';

// API base URL - points to Railway backend
// Set VITE_API_URL environment variable in Vercel to your Railway backend URL
// Example: https://depression-dashboard-production.up.railway.app
const API_BASE = import.meta.env.VITE_API_URL || 'https://depression-dashboard-production.up.railway.app';

export async function fetchDepression(): Promise<DepressionData> {
  const response = await fetch(`${API_BASE}/api/depression`);
  if (!response.ok) {
    let errorMessage = `Failed to fetch depression data (${response.status})`;
    if (response.status === 502) {
      errorMessage = 'Backend server is down (502). Please check Railway deployment.';
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
  return response.json();
}

export async function fetchTeams(): Promise<TeamsData> {
  const response = await fetch(`${API_BASE}/api/teams`);
  if (!response.ok) {
    let errorMessage = `Failed to fetch teams data (${response.status})`;
    if (response.status === 502) {
      errorMessage = 'Backend server is down (502). Please check Railway deployment.';
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
  return response.json();
}

export async function fetchRecentGames(): Promise<RecentGamesData> {
  const response = await fetch(`${API_BASE}/api/recent-games`);
  if (!response.ok) {
    let errorMessage = `Failed to fetch recent games (${response.status})`;
    if (response.status === 502) {
      errorMessage = 'Backend server is down (502). Please check Railway deployment.';
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
  return response.json();
}

export async function fetchUpcomingEvents(): Promise<UpcomingEventsData> {
  const response = await fetch(`${API_BASE}/api/upcoming-events`);
  if (!response.ok) {
    let errorMessage = `Failed to fetch upcoming events (${response.status})`;
    if (response.status === 502) {
      errorMessage = 'Backend server is down (502). Please check Railway deployment.';
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
  return response.json();
}

export async function refreshData(): Promise<void> {
  const response = await fetch(`${API_BASE}/api/refresh`, { method: 'POST' });
  if (!response.ok) {
    let errorMessage = `Failed to refresh data (${response.status})`;
    if (response.status === 502) {
      errorMessage = 'Backend server is down (502). Please check Railway deployment.';
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
}

