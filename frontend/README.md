# Depression Dashboard - Frontend

React + TypeScript + Tailwind CSS dashboard for visualizing the depression calculator.

## Quick Start

```bash
npm install
npm run dev
```

Visit `http://localhost:3000`

## Build for Production

```bash
npm run build
npm run preview
```

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Chart.js** - Data visualization
- **React Chart.js 2** - React wrapper for Chart.js

## Project Structure

```
frontend/
├── src/
│   ├── components/      # React components
│   │   ├── DepressionScoreCard.tsx
│   │   ├── TeamCard.tsx
│   │   ├── GameTimeline.tsx
│   │   ├── DepressionBreakdown.tsx
│   │   └── Header.tsx
│   ├── types/           # TypeScript type definitions
│   ├── api.ts           # API client functions
│   ├── App.tsx          # Main app component
│   ├── main.tsx         # Entry point
│   └── index.css        # Global styles
├── public/              # Static assets
└── package.json
```

## Components

- **DepressionScoreCard**: Hero card showing main depression score
- **TeamCard**: Individual team performance cards
- **GameTimeline**: Recent games and events timeline
- **DepressionBreakdown**: Charts showing breakdown of depression sources
- **Header**: Top navigation with refresh button

## Features

- Real-time data updates (auto-refresh every 60s)
- Responsive design (mobile, tablet, desktop)
- Interactive charts and visualizations
- Smooth animations and transitions
- Dark theme with team-specific colors

