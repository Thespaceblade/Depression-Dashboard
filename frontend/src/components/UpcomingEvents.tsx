import type { UpcomingEvent } from '../types';
import { getSportIcon } from '../utils/icons';
import { HiClock } from 'react-icons/hi2';

interface Props {
  events: UpcomingEvent[];
}

export default function UpcomingEvents({ events }: Props) {
  if (events.length === 0) {
    return (
      <div className="bg-card-bg rounded-2xl p-6 border-2 border-gray-700">
        <div className="flex items-center gap-2 mb-4">
          <HiClock className="text-blue-400" size={28} />
          <h2 className="text-2xl font-bold text-white">Upcoming Events</h2>
        </div>
        <p className="text-gray-400">No upcoming events scheduled</p>
      </div>
    );
  }

  return (
    <div className="bg-card-bg rounded-2xl p-6 border-2 border-gray-700">
      <div className="flex items-center gap-2 mb-6">
        <HiClock className="text-blue-400" size={28} />
        <h2 className="text-2xl font-bold text-white">Upcoming Events</h2>
      </div>
      
      <div className="space-y-4">
        {events.map((event, idx) => (
          <div
            key={idx}
            className="flex items-start gap-4 p-4 bg-gray-800 bg-opacity-50 rounded-lg hover:bg-opacity-70 transition-all duration-200 animate-fade-in border-l-4 border-blue-500"
            style={{ animationDelay: `${idx * 0.1}s` }}
          >
            {/* Sport Icon */}
            <div className="flex items-center justify-center flex-shrink-0 mt-1">
              {getSportIcon(event.sport, 24)}
            </div>
            
            {/* Content */}
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span className="font-semibold text-white">{event.team}</span>
                <span className="text-gray-500">vs</span>
                <span className="font-semibold text-blue-400">{event.opponent}</span>
                {event.is_home && (
                  <span className="text-xs bg-green-600 text-white px-2 py-1 rounded-full">
                    HOME
                  </span>
                )}
                {!event.is_home && (
                  <span className="text-xs bg-orange-600 text-white px-2 py-1 rounded-full">
                    AWAY
                  </span>
                )}
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-400">
                <HiClock size={16} />
                <span>{event.date}</span>
                <span className="text-gray-600">•</span>
                <span>{event.sport}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

