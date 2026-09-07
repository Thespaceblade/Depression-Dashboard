import type { Game } from '../types';

interface Props {
  games: Game[];
}

const resultClass = (result: string): string => {
  if (result === 'W' || result === 'P1') return 'text-win';
  if (result === 'L' || result === 'DNF') return 'text-loss';
  if (result.startsWith('P')) return 'text-led';
  return 'text-muted';
};

export default function GameTimeline({ games }: Props) {
  return (
    <section>
      <h2 className="section-title mb-1">Recent results</h2>
      <p className="label-caps mb-6">Verified games only</p>

      {games.length === 0 ? (
        <p className="text-muted text-sm">No verified recent games to display.</p>
      ) : (
        <ul className="divide-y divide-line border-t border-line">
          {games.slice(0, 10).map((game, idx) => (
            <li key={idx} className="py-4 flex flex-col sm:flex-row sm:items-baseline gap-1 sm:gap-4">
              <span className={`font-mono text-sm tabular-nums w-10 flex-shrink-0 ${resultClass(game.result)}`}>
                {game.result}
              </span>
              <div className="min-w-0 flex-1">
                <p className="text-ink font-medium">
                  {game.team}
                  {game.is_rivalry && (
                    <span className="ml-2 font-mono text-xs uppercase tracking-wider text-loss">
                      Rivalry
                    </span>
                  )}
                </p>
                <p className="text-xs text-muted mt-0.5">
                  <span className="uppercase tracking-wider">{game.sport}</span>
                  <span className="mx-2 opacity-40">·</span>
                  {game.date}
                </p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
