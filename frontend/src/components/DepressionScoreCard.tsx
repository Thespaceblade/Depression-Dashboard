import { useState } from 'react';
import type { DepressionData } from '../types';
import { getMoodImageUrl } from '../utils/icons';

interface Props {
  data: DepressionData;
}

export default function DepressionScoreCard({ data }: Props) {
  const [showInfo, setShowInfo] = useState(false);
  const moodUrl = getMoodImageUrl(data.score);

  return (
    <>
      <section className="relative w-full overflow-hidden animate-flood-in">
        {/* Atmosphere only — mood photo is a reaction box, not the hero plane */}
        <div className="absolute inset-0 bg-gradient-to-br from-flood via-field to-field" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_20%_0%,rgba(255,176,0,0.16),transparent_50%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_90%_80%,rgba(61,220,132,0.06),transparent_45%)]" />

        <div className="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 pt-20 sm:pt-24 pb-12 sm:pb-16">
          <div className="grid lg:grid-cols-[minmax(0,1.35fr)_minmax(0,0.85fr)] gap-8 lg:gap-12 items-end">
            <div>
              <p className="label-caps text-led mb-3">Live emotional scoreboard</p>
              <h1 className="font-display text-4xl sm:text-6xl md:text-7xl lg:text-8xl uppercase leading-[0.95] tracking-tight text-ink">
                Depression
                <br />
                Dashboard
              </h1>

              <div className="mt-8 sm:mt-10 flex flex-col sm:flex-row sm:items-end gap-4 sm:gap-8">
                <div className="animate-score-tick">
                  <p className="label-caps mb-1">Score</p>
                  <p className="font-mono text-6xl sm:text-7xl md:text-8xl font-semibold tabular-nums text-led leading-none">
                    {data.score.toFixed(1)}
                  </p>
                </div>
                <div className="pb-1 sm:pb-2">
                  <p className="font-display text-2xl sm:text-3xl uppercase text-ink tracking-wide">
                    {data.level}
                  </p>
                  <p className="mt-2 max-w-md text-sm sm:text-base text-muted leading-relaxed">
                    How Jason&apos;s teams are treating his mood right now — current season hits harder than last season&apos;s leftovers.
                  </p>
                  <button
                    type="button"
                    onClick={() => setShowInfo(true)}
                    className="util-link mt-3 inline-block border-b border-led/40 pb-0.5 hover:border-led"
                    aria-label="Learn more about the depression score"
                  >
                    How the score works
                  </button>
                </div>
              </div>
            </div>

            {moodUrl && (
              <aside className="justify-self-start lg:justify-self-end w-full max-w-sm">
                <p className="label-caps text-muted mb-2">Reaction</p>
                <figure className="border border-line bg-panel/40 overflow-hidden">
                  <img
                    src={moodUrl}
                    alt={`Mood reaction: ${data.level}`}
                    className="block w-full aspect-[4/5] object-cover"
                  />
                  <figcaption className="px-3 py-2 border-t border-line font-mono text-xs uppercase tracking-wider text-muted">
                    {data.level}
                  </figcaption>
                </figure>
              </aside>
            )}
          </div>
        </div>
      </section>

      {showInfo && (
        <div
          className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-4 bg-field/80"
          onClick={() => setShowInfo(false)}
        >
          <div
            className="bg-panel border border-line w-full sm:max-w-lg max-h-[85vh] overflow-y-auto p-5 sm:p-8"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-start justify-between gap-4 mb-5">
              <h3 className="font-display text-xl sm:text-2xl uppercase text-ink tracking-wide">
                About the score
              </h3>
              <button
                type="button"
                onClick={() => setShowInfo(false)}
                className="util-link"
                aria-label="Close"
              >
                Close
              </button>
            </div>

            <div className="space-y-5 text-sm sm:text-base text-muted leading-relaxed section-rule pt-5">
              <div>
                <p className="label-caps text-led mb-2">What it means</p>
                <p>
                  The depression score measures how Jason&apos;s teams&apos; recent performance is affecting his mood.
                  Lower (0-10) is elated; higher scores mean more sports-related disappointment, up to 100 (devastated).
                  Each 10-point band is a different emotional state.
                </p>
              </div>
              <div className="section-rule pt-5">
                <p className="label-caps text-led mb-2">How it works</p>
                <p>
                  Recent games, losses, rivalries, blowouts, and expectation gaps across Jason&apos;s teams feed the score.
                  Newer results weigh more. Prior-season and deep-offseason records fade the longer those games are behind him.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
