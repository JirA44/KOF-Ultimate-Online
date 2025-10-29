// KOF Ultimate Online - Application JavaScript

// Configuration
const API_BASE = 'http://localhost:3000/api';
const WS_URL = 'ws://localhost:3000';

let ws = null;
let reconnectInterval = null;

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 KOF Ultimate Online - App started');

    // Charger les stats initiales
    loadStats();
    loadTopPlayers();
    checkServerStatus();

    // Connecter WebSocket pour les mises à jour en temps réel
    connectWebSocket();

    // Refresh périodique
    setInterval(loadStats, 10000); // Toutes les 10 secondes
    setInterval(checkServerStatus, 5000); // Toutes les 5 secondes
});

// Connexion WebSocket
function connectWebSocket() {
    try {
        ws = new WebSocket(WS_URL);

        ws.onopen = () => {
            console.log('✅ WebSocket connecté');
            if (reconnectInterval) {
                clearInterval(reconnectInterval);
                reconnectInterval = null;
            }
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                handleWebSocketMessage(data);
            } catch (e) {
                console.error('Erreur parsing WebSocket message:', e);
            }
        };

        ws.onerror = (error) => {
            console.error('❌ WebSocket erreur:', error);
        };

        ws.onclose = () => {
            console.log('⚠️ WebSocket déconnecté');
            // Tentative de reconnexion
            if (!reconnectInterval) {
                reconnectInterval = setInterval(() => {
                    console.log('🔄 Tentative de reconnexion...');
                    connectWebSocket();
                }, 5000);
            }
        };

    } catch (error) {
        console.error('❌ Impossible de connecter WebSocket:', error);
    }
}

// Gestion des messages WebSocket
function handleWebSocketMessage(data) {
    const { type } = data;

    if (type === 'stats') {
        updateStatsUI(data.data);
    } else if (type === 'leaderboard') {
        updateLeaderboardUI(data.data);
    }
}

// Charger les stats via API
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const result = await response.json();

        if (result.success) {
            updateStatsUI(result.data);
        }
    } catch (error) {
        console.error('Erreur chargement stats:', error);
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
            // Animation du compteur
            animateValue(element, parseInt(element.textContent) || 0, value, 500);
        }
    });
}

// Animation des nombres
function animateValue(element, start, end, duration) {
    if (start === end) return;

    const range = end - start;
    const increment = range / (duration / 16); // 60 FPS
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

// Charger le top 10 des joueurs
async function loadTopPlayers() {
    try {
        const response = await fetch(`${API_BASE}/leaderboard`);
        const result = await response.json();

        if (result.success) {
            updateLeaderboardUI(result.data.slice(0, 10));
        }
    } catch (error) {
        console.error('Erreur chargement leaderboard:', error);
        const container = document.getElementById('top-players');
        if (container) {
            container.innerHTML = '<div class="error">Erreur de chargement du classement</div>';
        }
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

// Vérifier le statut du serveur
async function checkServerStatus() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const result = await response.json();

        const statusIndicator = document.getElementById('server-status');
        const statusText = document.getElementById('server-status-text');

        if (statusIndicator && statusText) {
            if (result.success && result.status === 'running') {
                statusIndicator.className = 'status-indicator online';
                statusText.textContent = result.battlenet ?
                    'En ligne (Battle.net connecté)' :
                    'En ligne (Battle.net déconnecté)';
            } else {
                statusIndicator.className = 'status-indicator offline';
                statusText.textContent = 'Hors ligne';
            }
        }
    } catch (error) {
        const statusIndicator = document.getElementById('server-status');
        const statusText = document.getElementById('server-status-text');

        if (statusIndicator && statusText) {
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
