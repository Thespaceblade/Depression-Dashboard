
import Foundation

struct DepressionData: Codable, Sendable {
    let success: Bool
    let score: Double
    let level: String
    let emoji: String
    let breakdown: [String: DepressionBreakdownEntry]
    let timestamp: String
}

struct DepressionBreakdownEntry: Codable, Sendable {
    let score: Double
    let details: [String: Double]?
    let record: String?
    let position: String?
}

struct TeamsData: Codable, Sendable {
    let success: Bool
    let teams: [Team]
    let timestamp: String
}

struct Team: Codable, Identifiable, Sendable {
    var id: String { name + sport }

    let name: String
    let sport: String
    let wins: Int
    let losses: Int
    let record: String
    let win_percentage: Double
    let recent_streak: [String]
    let depression_points: Double
    let breakdown: [String: Double]
    let expected_performance: Double?
    let jasons_expectations: Double?
    let rivals: [String]?
    let recent_rivalry_losses: [String]?
    let interest_level: Double?
    let notes: String?
    let championship_position: Int?
    let recent_dnfs: Int?
}

struct Game: Codable, Identifiable, Sendable {
    var id: String { (datetime ?? date) + team + (opponent ?? "") }

    let date: String
    let datetime: String?
    let team: String
    let sport: String
    let result: String
    let type: String
    let opponent: String?
    let team_score: Int?
    let opponent_score: Int?
    let score_margin: Int?
    let is_home: Bool?
    let is_overtime: Bool?
    let is_rivalry: Bool?
}

struct RecentGamesData: Codable, Sendable {
    let success: Bool
    let games: [Game]
    let timestamp: String
}

struct UpcomingEvent: Codable, Identifiable, Sendable {
    var id: String {
        let dateStr = datetime ?? date
        return "\(dateStr)-\(team)-\(opponent)-\(sport)"
    }

    let date: String
    let datetime: String?
    let team: String
    let sport: String
    let opponent: String
    let type: String
    let is_home: Bool?
}

struct UpcomingEventsData: Codable, Sendable {
    let success: Bool
    let events: [UpcomingEvent]
    let timestamp: String
}


