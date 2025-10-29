#!/usr/bin/env node
/**
 * KOF ULTIMATE ONLINE - Serveur Web
 * Interface web pour le système Battle.net
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const WebSocket = require('ws');

const PORT = 3000;
const BATTLENET_WS_URL = 'ws://localhost:8765';

// État du serveur
const serverState = {
    players: [],
    matches: [],
    stats: {
        totalPlayers: 0,
        onlinePlayers: 0,
        activeMatches: 0,
        totalMatches: 0
    },
    lastUpdate: new Date()
};

// Connexion au serveur Battle.net pour récupérer les stats
let battlenetConnection = null;

function connectToBattleNet() {
    try {
        battlenetConnection = new WebSocket(BATTLENET_WS_URL);

        battlenetConnection.on('open', () => {
            console.log('✅ Connecté au serveur Battle.net');

            // S'authentifier comme observateur
            battlenetConnection.send(JSON.stringify({
                type: 'auth',
                username: 'WebServer',
                player_id: 'web_observer'
            }));
        });

        battlenetConnection.on('message', (data) => {
            try {
                const message = JSON.parse(data);
                handleBattleNetMessage(message);
            } catch (e) {
                console.error('Erreur parsing message:', e);
            }
        });

        battlenetConnection.on('error', (error) => {
            console.error('❌ Erreur Battle.net:', error.message);
        });

        battlenetConnection.on('close', () => {
            console.log('⚠️ Déconnecté du serveur Battle.net');
            // Reconnexion après 5 secondes
            setTimeout(connectToBattleNet, 5000);
        });

    } catch (error) {
        console.error('❌ Impossible de se connecter au serveur Battle.net');
        setTimeout(connectToBattleNet, 5000);
    }
}

function handleBattleNetMessage(message) {
    const { type } = message;

    if (type === 'server_stats') {
        serverState.stats = {
            totalPlayers: message.total_players || 0,
            onlinePlayers: message.online_players || 0,
            activeMatches: message.active_matches || 0,
            totalMatches: message.total_matches || 0
        };
        serverState.lastUpdate = new Date();
    } else if (type === 'leaderboard') {
        serverState.players = message.players || [];
    } else if (type === 'online_players') {
        serverState.players = message.players || [];
    }
}

// Types MIME
const mimeTypes = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'text/javascript',
    '.json': 'application/json',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.gif': 'image/gif',
    '.svg': 'image/svg+xml',
    '.ico': 'image/x-icon'
};

// Serveur HTTP
const server = http.createServer((req, res) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);

    // API Routes
    if (req.url.startsWith('/api/')) {
        handleApiRequest(req, res);
        return;
    }

    // Routes statiques
    let filePath = req.url === '/' ? '/web/index.html' : `/web${req.url}`;
    filePath = path.join(__dirname, filePath);

    const extname = String(path.extname(filePath)).toLowerCase();
    const contentType = mimeTypes[extname] || 'application/octet-stream';

    fs.readFile(filePath, (error, content) => {
        if (error) {
            if (error.code === 'ENOENT') {
                res.writeHead(404, { 'Content-Type': 'text/html' });
                res.end('<h1>404 - Page non trouvée</h1>', 'utf-8');
            } else {
                res.writeHead(500);
                res.end(`Erreur serveur: ${error.code}`, 'utf-8');
            }
        } else {
            res.writeHead(200, { 'Content-Type': contentType });
            res.end(content, 'utf-8');
        }
    });
});

// API Endpoints
function handleApiRequest(req, res) {
    res.setHeader('Content-Type', 'application/json');
    res.setHeader('Access-Control-Allow-Origin', '*');

    const url = req.url;

    if (url === '/api/stats') {
        // Stats du serveur
        res.writeHead(200);
        res.end(JSON.stringify({
            success: true,
            data: serverState.stats,
            lastUpdate: serverState.lastUpdate
        }));

    } else if (url === '/api/leaderboard') {
        // Classement
        res.writeHead(200);
        res.end(JSON.stringify({
            success: true,
            data: serverState.players.slice(0, 100) // Top 100
        }));

    } else if (url === '/api/players') {
        // Joueurs en ligne
        res.writeHead(200);
        res.end(JSON.stringify({
            success: true,
            data: serverState.players
        }));

    } else if (url === '/api/health') {
        // Health check
        res.writeHead(200);
        res.end(JSON.stringify({
            success: true,
            status: 'running',
            battlenet: battlenetConnection && battlenetConnection.readyState === WebSocket.OPEN
        }));

    } else {
        res.writeHead(404);
        res.end(JSON.stringify({
            success: false,
            error: 'Endpoint non trouvé'
        }));
    }
}

// WebSocket pour les mises à jour en temps réel
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
    console.log('🔗 Nouveau client web connecté');

    // Envoyer les stats initiales
    ws.send(JSON.stringify({
        type: 'stats',
        data: serverState.stats
    }));

    ws.send(JSON.stringify({
        type: 'leaderboard',
        data: serverState.players.slice(0, 100)
    }));

    // Heartbeat
    const interval = setInterval(() => {
        if (ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({
                type: 'stats',
                data: serverState.stats
            }));
        }
    }, 5000); // Toutes les 5 secondes

    ws.on('close', () => {
        console.log('❌ Client web déconnecté');
        clearInterval(interval);
    });
});

// Démarrage
server.listen(PORT, () => {
    console.log('\n╔═══════════════════════════════════════════════════════════╗');
    console.log('║                                                           ║');
    console.log('║         🌐 KOF ULTIMATE ONLINE - SERVEUR WEB 🌐          ║');
    console.log('║                                                           ║');
    console.log('╚═══════════════════════════════════════════════════════════╝\n');
    console.log(`🚀 Serveur démarré sur: http://localhost:${PORT}`);
    console.log(`📊 Dashboard: http://localhost:${PORT}/dashboard.html`);
    console.log(`🏆 Classement: http://localhost:${PORT}/leaderboard.html`);
    console.log(`\n📡 API disponibles:`);
    console.log(`   - GET /api/stats`);
    console.log(`   - GET /api/leaderboard`);
    console.log(`   - GET /api/players`);
    console.log(`   - GET /api/health`);
    console.log(`\n🔌 WebSocket pour updates temps réel: ws://localhost:${PORT}`);
    console.log(`\n⏳ Connexion au serveur Battle.net...`);

    // Se connecter au serveur Battle.net
    connectToBattleNet();

    // Demander les stats régulièrement
    setInterval(() => {
        if (battlenetConnection && battlenetConnection.readyState === WebSocket.OPEN) {
            battlenetConnection.send(JSON.stringify({ type: 'get_leaderboard' }));
        }
    }, 10000); // Toutes les 10 secondes
});

// Gestion des erreurs
process.on('uncaughtException', (error) => {
    console.error('❌ Erreur non gérée:', error);
});

process.on('SIGINT', () => {
    console.log('\n\n🛑 Arrêt du serveur web...');
    if (battlenetConnection) {
        battlenetConnection.close();
    }
    server.close(() => {
        console.log('👋 Serveur web arrêté');
        process.exit(0);
    });
});
