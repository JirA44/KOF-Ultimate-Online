// KOF Ultimate Online - API Mock pour version statique (Cloudflare Pages)
// Simule les données du serveur pour la démo en ligne

const API_MOCK = {
    stats: {
        onlinePlayers: 8,
        activeMatches: 3,
        totalMatches: 127,
        totalPlayers: 45
    },

    leaderboard: [
        { id: 1, username: "DragonKing", elo: 2580, wins: 89, losses: 12, win_rate: 88.1, status: "online" },
        { id: 2, username: "ShadowFist", elo: 2420, wins: 76, losses: 18, win_rate: 80.9, status: "online" },
        { id: 3, username: "FirePhoenix", elo: 2190, wins: 65, losses: 22, win_rate: 74.7, status: "offline" },
        { id: 4, username: "IceQueen", elo: 2050, wins: 58, losses: 25, win_rate: 69.9, status: "online" },
        { id: 5, username: "ThunderBolt", elo: 1890, wins: 52, losses: 31, win_rate: 62.7, status: "offline" },
        { id: 6, username: "BlazeMaster", elo: 1750, wins: 45, losses: 35, win_rate: 56.3, status: "online" },
        { id: 7, username: "NightHawk", elo: 1620, wins: 41, losses: 39, win_rate: 51.3, status: "offline" },
        { id: 8, username: "StormRider", elo: 1480, wins: 38, losses: 42, win_rate: 47.5, status: "online" },
        { id: 9, username: "CrimsonStar", elo: 1350, wins: 32, losses: 48, win_rate: 40.0, status: "offline" },
        { id: 10, username: "MysticSage", elo: 1220, wins: 28, losses: 52, win_rate: 35.0, status: "online" },
        { id: 11, username: "GoldenFalcon", elo: 1180, wins: 25, losses: 45, win_rate: 35.7, status: "offline" },
        { id: 12, username: "SilverWolf", elo: 1150, wins: 24, losses: 46, win_rate: 34.3, status: "online" },
        { id: 13, username: "IronFist", elo: 1090, wins: 22, losses: 48, win_rate: 31.4, status: "offline" },
        { id: 14, username: "CrystalBlade", elo: 1050, wins: 20, losses: 50, win_rate: 28.6, status: "online" },
        { id: 15, username: "VenomStrike", elo: 980, wins: 18, losses: 52, win_rate: 25.7, status: "offline" },
        { id: 16, username: "EmeraldKnight", elo: 920, wins: 16, losses: 54, win_rate: 22.9, status: "offline" },
        { id: 17, username: "RubyWarrior", elo: 870, wins: 14, losses: 56, win_rate: 20.0, status: "offline" },
        { id: 18, username: "SapphireGuard", elo: 820, wins: 12, losses: 58, win_rate: 17.1, status: "offline" },
        { id: 19, username: "AmberRogue", elo: 780, wins: 10, losses: 60, win_rate: 14.3, status: "offline" },
        { id: 20, username: "JadeMonk", elo: 740, wins: 8, losses: 62, win_rate: 11.4, status: "offline" }
    ],

    serverHealth: {
        success: true,
        status: "demo",
        battlenet: false,
        message: "Version démo - Données simulées"
    }
};

// Fonction pour récupérer les stats
function getMockStats() {
    return {
        success: true,
        data: API_MOCK.stats,
        lastUpdate: new Date().toISOString()
    };
}

// Fonction pour récupérer le classement
function getMockLeaderboard() {
    return {
        success: true,
        data: API_MOCK.leaderboard
    };
}

// Fonction pour récupérer les joueurs en ligne
function getMockPlayers() {
    return {
        success: true,
        data: API_MOCK.leaderboard.filter(p => p.status === "online")
    };
}

// Fonction pour le health check
function getMockHealth() {
    return API_MOCK.serverHealth;
}

// Export pour utilisation
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        getMockStats,
        getMockLeaderboard,
        getMockPlayers,
        getMockHealth
    };
}
