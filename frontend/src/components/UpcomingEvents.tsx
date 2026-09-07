import type { UpcomingEvent } from '../types';

interface Props {
  events: UpcomingEvent[];
}

export default function UpcomingEvents({ events }: Props) {
  return (
    <section>
      <h2 className="section-title mb-1">Upcoming</h2>
      <p className="label-caps mb-6">Next on the schedule</p>

      {events.length === 0 ? (
        <p className="text-muted text-sm">No upcoming events scheduled.</p>
      ) : (
        <ul className="divide-y divide-line border-t border-line">
          {events.map((event, idx) => (
            <li key={idx} className="py-4 flex flex-col sm:flex-row sm:items-baseline gap-1 sm:gap-6">
              <span className="font-mono text-xs text-led uppercase tracking-wider w-14 flex-shrink-0">
                {event.is_home ? 'Home' : 'Away'}
              </span>
              <div className="min-w-0 flex-1">
                <p className="text-ink">
                  <span className="font-medium">{event.team}</span>
                  <span className="text-muted mx-2">vs</span>
                  <span className="font-medium">{event.opponent}</span>
                </p>
                <p className="text-xs text-muted mt-0.5">
                  <span className="uppercase tracking-wider">{event.sport}</span>
                  <span className="mx-2 opacity-40">·</span>
                  {event.date}
                </p>
              </div>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
