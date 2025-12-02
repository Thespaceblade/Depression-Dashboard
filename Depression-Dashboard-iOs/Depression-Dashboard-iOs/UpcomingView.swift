import SwiftUI

struct UpcomingView: View {
    @State private var data: UpcomingEventsData?
    @State private var isLoading = false
    @State private var errorMessage: String?

    var body: some View {
        NavigationView {
            Group {
                if isLoading && data == nil {
                    ProgressView()
                        .tint(.blue)
                } else {
                    List {
                        if let errorMessage {
                            Section {
                                Text(errorMessage)
                                    .foregroundColor(.red)
                            }
                        }

                        if let events = data?.events, !events.isEmpty {
                            ForEach(events) { event in
                                EventRow(event: event)
                                    .listRowBackground(Color(red: 0.11, green: 0.11, blue: 0.19))
                            }
                        } else {
                            Text("No upcoming events scheduled")
                                .foregroundColor(.gray)
                        }
                    }
                    .listStyle(.insetGrouped)
                    .background(Color(red: 0.06, green: 0.06, blue: 0.12))
                    .refreshable {
                        await load()
                    }
                }
            }
            .navigationTitle("Upcoming")
            .task {
                await load()
            }
        }
    }

    private func load() async {
        guard !isLoading else { return }
        isLoading = true
        defer { isLoading = false }

        do {
            let result = try await APIClient.shared.fetchUpcomingEvents()
            await MainActor.run {
                self.data = result
                self.errorMessage = nil
            }
        } catch {
            await MainActor.run {
                self.errorMessage = "Failed to load upcoming events: \(error.localizedDescription)"
                print("Upcoming events error: \(error)")
            }
        }
    }
}

private struct EventRow: View {
    let event: UpcomingEvent

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack(spacing: 8) {
                Image(systemName: "calendar.badge.clock")
                    .foregroundColor(.blue)

                Text(event.team)
                    .font(.subheadline.bold())
                    .foregroundColor(.white)

                Text("vs \(event.opponent)")
                    .font(.caption)
                    .foregroundColor(.blue)

                Spacer()

                Text(event.sport)
                    .font(.caption2)
                    .foregroundColor(.gray)
            }

            HStack(spacing: 4) {
                let dateString = event.datetime ?? event.date
                if !dateString.isEmpty {
                    if let date = parseDate(dateString) {
                        Text(date, style: .date)
                        Text(date, style: .time)
                    } else {
                        Text(dateString)
                    }
                } else {
                    Text("Date TBD")
                }

                if !event.type.isEmpty {
                    Text("•")
                    Text(event.type)
                }

                if let isHome = event.is_home {
                    Text("•")
                    Text(isHome ? "HOME" : "AWAY")
                }
            }
            .font(.caption)
            .foregroundColor(.gray)
        }
        .padding(.vertical, 6)
    }

    private func parseDate(_ dateString: String) -> Date? {
        let isoFormatter = ISO8601DateFormatter()
        isoFormatter.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
        if let date = isoFormatter.date(from: dateString) {
            return date
        }
        
        isoFormatter.formatOptions = [.withInternetDateTime]
        if let date = isoFormatter.date(from: dateString) {
            return date
        }
        
        let rfc3339Formatter = DateFormatter()
        rfc3339Formatter.dateFormat = "yyyy-MM-dd'T'HH:mm:ssZ"
        if let date = rfc3339Formatter.date(from: dateString) {
            return date
        }
        
        let simpleFormatter = DateFormatter()
        simpleFormatter.dateFormat = "yyyy-MM-dd"
        if let date = simpleFormatter.date(from: dateString) {
            return date
        }
        
        return nil
    }
}


