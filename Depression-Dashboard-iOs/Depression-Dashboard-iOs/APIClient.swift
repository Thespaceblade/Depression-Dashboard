import Foundation

actor APIClient {
    static let shared = APIClient()

    private let baseURL = URL(string: "https://depression-dashboard-production.up.railway.app")!
   
    nonisolated private static let decoder: JSONDecoder = {
        let d = JSONDecoder()
        return d
    }()

    private func get<T: Decodable>(_ path: String) async throws -> T {
        let url = baseURL.appendingPathComponent(path)
        let (data, response) = try await URLSession.shared.data(from: url)

        guard let http = response as? HTTPURLResponse,
              200..<300 ~= http.statusCode else {
            throw URLError(.badServerResponse)
        }

        return try Self.decoder.decode(T.self, from: data)
    }

    private func post(_ path: String) async throws {
        let url = baseURL.appendingPathComponent(path)
        var request = URLRequest(url: url)
        request.httpMethod = "POST"

        let (_, response) = try await URLSession.shared.data(for: request)
        guard let http = response as? HTTPURLResponse,
              200..<300 ~= http.statusCode else {
            throw URLError(.badServerResponse)
        }
    }


    func fetchDepression() async throws -> DepressionData {
        try await get("/api/depression")
    }

    func fetchRecentGames() async throws -> RecentGamesData {
        try await get("/api/recent-games")
    }

    func fetchUpcomingEvents() async throws -> UpcomingEventsData {
        try await get("/api/upcoming-events")
    }

    func refreshData() async throws {
        try await post("/api/refresh")
    }
}

