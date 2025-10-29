// KOF Ultimate Online - Application JavaScript (Version Statique pour Cloudflare)
// Version sans serveur Node.js - Utilise des données mockées

// Configuration
const USE_MOCK_DATA = true; // Toujours vrai pour la version statique

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 KOF Ultimate Online - Version Statique');

    // Afficher le message démo
    showDemoNotice();

    // Charger les stats mockées
    loadMockStats();
    loadMockTopPlayers();
    checkMockServerStatus();

    // Simuler les mises à jour temps réel
    setInterval(loadMockStats, 10000); // Toutes les 10 secondes
    setInterval(() => {
        // Variation aléatoire des stats pour simuler l'activité
        API_MOCK.stats.onlinePlayers = 5 + Math.floor(Math.random() * 10);
        API_MOCK.stats.activeMatches = Math.floor(Math.random() * 5);
        loadMockStats();
    }, 15000);
});

// Afficher une notice pour la version démo
function showDemoNotice() {
    const notice = document.createElement('div');
    notice.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: rgba(255, 170, 0, 0.9);
        color: #0a0e27;
        padding: 15px 25px;
        border-radius: 10px;
        font-weight: bold;
        z-index: 10000;
        box-shadow: 0 5px 20px rgba(255, 170, 0, 0.4);
        animation: slideIn 0.5s ease;
    `;
    notice.innerHTML = '🌐 Version Démo - Données Simulées';
    document.body.appendChild(notice);

    // Retirer après 5 secondes
    setTimeout(() => {
        notice.style.animation = 'slideOut 0.5s ease';
        setTimeout(() => notice.remove(), 500);
    }, 5000);

    // Ajouter les animations CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(400px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOut {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(400px); opacity: 0; }
        }
    `;
    document.head.appendChild(style);
}

// Charger les stats mockées
function loadMockStats() {
    const stats = getMockStats();
    if (stats.success) {
        updateStatsUI(stats.data);
    }
}

// Mettre à jour l'UI des stats
function updateStatsUI(stats) {
    const elements = {
        'online-players': stats.onlinePlayers || 0,
        'active-matches': stats.activeMatches || 0,
        'total-matches': stats.totalMatches || 0,
        'total-players': stats.totalPlayers || 0
    };

    Object.entries(elements).forEach(([id, value]) => {
        const element = document.getElementById(id);
        if (element) {
            animateValue(element, parseInt(element.textContent) || 0, value, 500);
        }
    });
}

// Animation des nombres
function animateValue(element, start, end, duration) {
    if (start === end) return;

    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;

        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }

        element.textContent = Math.round(current);
    }, 16);
}

// Charger le top 10 mockés
function loadMockTopPlayers() {
    const leaderboard = getMockLeaderboard();
    if (leaderboard.success) {
        updateLeaderboardUI(leaderboard.data.slice(0, 10));
    }
}

// Mettre à jour l'UI du classement
function updateLeaderboardUI(players) {
    const container = document.getElementById('top-players');
    if (!container) return;

    if (!players || players.length === 0) {
        container.innerHTML = '<div class="no-data">Aucun joueur dans le classement</div>';
        return;
    }

    const html = `
        <table class="leaderboard-table">
            <thead>
                <tr>
                    <th>Rang</th>
                    <th>Joueur</th>
                    <th>ELO</th>
                    <th>V/D</th>
                    <th>Win Rate</th>
                </tr>
            </thead>
            <tbody>
                ${players.map((player, index) => `
                    <tr class="player-row rank-${index + 1}">
                        <td class="rank">
                            ${index + 1 <= 3 ? getMedalIcon(index + 1) : `#${index + 1}`}
                        </td>
                        <td class="username">${escapeHtml(player.username || 'Unknown')}</td>
                        <td class="elo">${player.elo || 1000}</td>
                        <td class="wl">${player.wins || 0}/${player.losses || 0}</td>
                        <td class="winrate">${(player.win_rate || 0).toFixed(1)}%</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    container.innerHTML = html;
}

// Icônes de médailles
function getMedalIcon(rank) {
    const medals = {
        1: '🥇',
        2: '🥈',
        3: '🥉'
    };
    return medals[rank] || `#${rank}`;
}

// Échapper le HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Vérifier le statut du serveur (mocké)
function checkMockServerStatus() {
    const health = getMockHealth();

    const statusIndicator = document.getElementById('server-status');
    const statusText = document.getElementById('server-status-text');

    if (statusIndicator && statusText) {
        if (health.success && health.status === 'demo') {
            statusIndicator.className = 'status-indicator online';
            statusText.textContent = health.message || 'Version démo';
        } else {
            statusIndicator.className = 'status-indicator offline';
            statusText.textContent = 'Hors ligne';
        }
    }
}

// Styles additionnels pour le tableau
const style = document.createElement('style');
style.textContent = `
    .leaderboard-table {
        width: 100%;
        border-collapse: collapse;
    }

    .leaderboard-table th {
        background: rgba(0, 212, 255, 0.2);
        padding: 15px;
        text-align: left;
        color: var(--primary);
        font-weight: bold;
    }

    .leaderboard-table td {
        padding: 12px 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .player-row:hover {
        background: rgba(0, 212, 255, 0.1);
    }

    .rank {
        font-weight: bold;
        font-size: 1.2em;
    }

    .rank-1 .rank { color: #ffd700; }
    .rank-2 .rank { color: #c0c0c0; }
    .rank-3 .rank { color: #cd7f32; }

    .username {
        color: var(--text);
        font-weight: 500;
    }

    .elo {
        color: var(--primary);
        font-weight: bold;
    }

    .wl {
        color: var(--text-secondary);
    }

    .winrate {
        color: var(--success);
        font-weight: bold;
    }

    .error, .no-data {
        padding: 40px;
        text-align: center;
        color: var(--text-secondary);
    }
`;
document.head.appendChild(style);
