
import SwiftUI

private func scoreLevelColor(_ score: Double) -> Color {
    switch score {
    case ..<10: return .green
    case ..<20: return .green
    case ..<30: return .yellow
    case ..<40: return .yellow
    case ..<50: return .gray
    case ..<60: return .orange
    case ..<70: return .orange
    case ..<80: return .red
    case ..<90: return .red.opacity(0.8)
    default:     return .red.opacity(0.9)
    }
}

struct OverviewView: View {
    @State private var data: DepressionData?
    @State private var isLoading = false
    @State private var errorMessage: String?

    var body: some View {
        NavigationView {
            Group {
                if isLoading && data == nil {
                    ProgressView()
                        .tint(.blue)
                } else {
                    ScrollView {
                        VStack(spacing: 16) {
                            if let errorMessage {
                                ErrorCard(message: errorMessage)
                            }

                            if let data {
                                ScoreCard(data: data)
                                BreakdownCard(data: data)
                            }
                        }
                        .padding()
                        .background(Color(red: 0.06, green: 0.06, blue: 0.12))
                    }
                    .refreshable {
                        await refresh()
                    }
                }
            }
            .navigationTitle("Depression Dashboard")
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
            let result = try await APIClient.shared.fetchDepression()
            await MainActor.run {
                self.data = result
                self.errorMessage = nil
            }
        } catch {
            await MainActor.run {
                self.errorMessage = "Failed to load data."
            }
        }
    }

    private func refresh() async {
        do {
            try await APIClient.shared.refreshData()
        } catch {
            // ignore, then reload
        }
        await load()
    }
}

private struct ScoreCard: View {
    let data: DepressionData

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            Text("Overall Depression Score")
                .font(.title3.bold())
                .foregroundColor(.white)

            Text("\(data.emoji) \(String(format: "%.1f", data.score))")
                .font(.system(size: 40, weight: .heavy, design: .rounded))
                .foregroundColor(.white)

            HStack {
                Text(data.level)
                    .font(.caption.bold())
                    .foregroundColor(.white)
                    .padding(.horizontal, 10)
                    .padding(.vertical, 4)
                    .background(scoreLevelColor(data.score))
                    .clipShape(Capsule())

                Spacer()

                Text("Updated \(formattedDate(data.timestamp))")
                    .font(.caption)
                    .foregroundColor(.gray)
            }

            GeometryReader { geo in
                ZStack(alignment: .leading) {
                    Capsule()
                        .fill(Color.white.opacity(0.1))
                        .frame(height: 8)

                    Capsule()
                        .fill(scoreLevelColor(data.score))
                        .frame(
                            width: geo.size.width * CGFloat(min(max(data.score, 0), 100) / 100.0),
                            height: 8
                        )
                }
            }
            .frame(height: 8)
        }
        .padding()
        .background(
            LinearGradient(
                gradient: Gradient(colors: [Color.blue.opacity(0.5), Color.purple.opacity(0.5)]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
        )
        .cornerRadius(20)
        .shadow(radius: 10)
    }

    private func formattedDate(_ isoString: String) -> String {
        let f = ISO8601DateFormatter()
        if let date = f.date(from: isoString) {
            let out = DateFormatter()
            out.dateStyle = .short
            out.timeStyle = .short
            return out.string(from: date)
        }
        return isoString
    }
}

private struct BreakdownCard: View {
    let data: DepressionData

    var sortedEntries: [(key: String, value: DepressionBreakdownEntry)] {
        data.breakdown.sorted { $0.value.score > $1.value.score }
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(spacing: 8) {
                Image(systemName: "chart.pie.fill")
                    .foregroundColor(.blue)
                Text("Depression Breakdown")
                    .font(.title3.bold())
                    .foregroundColor(.white)
            }

            ForEach(sortedEntries, id: \.key) { entry in
                HStack {
                    VStack(alignment: .leading, spacing: 4) {
                        Text(entry.key)
                            .font(.subheadline.bold())
                            .foregroundColor(.white)

                        if let record = entry.value.record {
                            Text(record)
                                .font(.caption)
                                .foregroundColor(.gray)
                        }

                        if let position = entry.value.position {
                            Text(position)
                                .font(.caption2)
                                .foregroundColor(.gray)
                        }
                    }

                    Spacer()

                    Text(String(format: "%.1f pts", entry.value.score))
                        .font(.subheadline.bold())
                        .foregroundColor(.red)
                }
                .padding(.vertical, 6)

                if entry.key != sortedEntries.last?.key {
                    Divider().background(Color.white.opacity(0.1))
                }
            }
        }
        .padding()
        .background(Color(red: 0.10, green: 0.10, blue: 0.18))
        .cornerRadius(16)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(Color.white.opacity(0.08), lineWidth: 1)
        )
    }
}

private struct ErrorCard: View {
    let message: String

    var body: some View {
        HStack(alignment: .top, spacing: 8) {
            Image(systemName: "exclamationmark.triangle.fill")
                .foregroundColor(.yellow)
            Text(message)
                .font(.subheadline)
                .foregroundColor(.white)
            Spacer()
        }
        .padding()
        .background(Color.red.opacity(0.3))
        .cornerRadius(12)
    }
}
