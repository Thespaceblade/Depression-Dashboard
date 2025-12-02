//
//  GamesView.swift
//  Depression-Dashboard-iOs
//
//  Created by Jason Charwin on 12/2/25.
//

import SwiftUI

struct GamesView: View {
    @State private var data: RecentGamesData?
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

                        if let games = data?.games, !games.isEmpty {
                            ForEach(games) { game in
                                GameRow(game: game)
                                    .listRowBackground(Color(red: 0.11, green: 0.11, blue: 0.19))
                            }
                        } else {
                            Text("No recent games to display")
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
            .navigationTitle("Recent Games")
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
            let result = try await APIClient.shared.fetchRecentGames()
            await MainActor.run {
                self.data = result
                self.errorMessage = nil
            }
        } catch {
            await MainActor.run {
                self.errorMessage = "Failed to load recent games."
            }
        }
    }
}

private struct GameRow: View {
    let game: Game

    var resultColor: Color {
        let r = game.result.uppercased()
        if r == "W" || r == "P1" { return .green }
        if r == "L" || r == "DNF" { return .red }
        if r.hasPrefix("P") { return .yellow }
        return .gray
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack(spacing: 8) {
                Circle()
                    .fill(resultColor)
                    .frame(width: 10, height: 10)

                Text(game.team)
                    .font(.subheadline.bold())
                    .foregroundColor(.white)

                if let opponent = game.opponent {
                    Text("vs \(opponent)")
                        .font(.caption)
                        .foregroundColor(.blue)
                }

                Spacer()

                Text(game.sport)
                    .font(.caption2)
                    .foregroundColor(.gray)
            }

            if let (scoreText, isLoss) = scoreString(game: game) {
                Text(scoreText)
                    .font(.subheadline.bold())
                    .foregroundColor(isLoss ? .red : .green)
            }

            HStack(spacing: 4) {
                if let date = parseDate(game.datetime ?? game.date) {
                    Text(date, style: .date)
                    Text(date, style: .time)
                } else {
                    Text(game.date)
                }

                if let isHome = game.is_home {
                    Text("•")
                    Text(isHome ? "Home" : "Away")
                }

                if game.is_overtime == true {
                    Text("• OT")
                }

                if game.is_rivalry == true {
                    Text("• Rivalry")
                }
            }
            .font(.caption)
            .foregroundColor(.gray)
        }
        .padding(.vertical, 6)
    }

    private func parseDate(_ iso: String) -> Date? {
        ISO8601DateFormatter().date(from: iso)
    }

    private func scoreString(game: Game) -> (String, Bool)? {
        guard let teamScore = game.team_score,
              let oppScore = game.opponent_score
        else { return nil }

        let text = "\(game.result) (\(teamScore)–\(oppScore))"
        let isLoss = game.result.uppercased().hasPrefix("L") || game.result.uppercased() == "DNF"
        return (text, isLoss)
    }
}
