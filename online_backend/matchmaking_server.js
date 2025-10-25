/**
 * KOF Ultimate Online - Matchmaking Server
 * Serveur WebSocket pour matchmaking en temps réel
 */

const WebSocket = require('ws');
const http = require('http');
const uuid = require('uuid');

const PORT = process.env.MATCHMAKING_PORT || 3101;

// Server HTTP pour health check
const server = http.createServer((req, res) => {
    if (req.url === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({
            status: 'online',
            service: 'KOF Matchmaking Server',
            players_online: connectedPlayers.size,
            matchmaking_queue: matchmakingQueue.length,
            active_matches: activeMatches.size
        }));
    } else {
        res.writeHead(200);
        res.end('KOF Ultimate Online - Matchmaking Server v2.0');
    }
});

// WebSocket Server
const wss = new WebSocket.Server({ server });

// State management
const connectedPlayers = new Map(); // playerId -> { ws, info }
const matchmakingQueue = [];        // [{playerId, elo, mode, timestamp}]
const activeMatches = new Map();    // matchId -> {player1, player2, status}
const customRooms = new Map();      // roomId -> {host, players, settings}

// ==================== UTILITY FUNCTIONS ====================

function broadcast(message, excludeWs = null) {
    wss.clients.forEach(client => {
        if (client !== excludeWs && client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify(message));
        }
    });
}

function sendToPlayer(playerId, message) {
    const playerData = connectedPlayers.get(playerId);
    if (playerData && playerData.ws.readyState === WebSocket.OPEN) {
        playerData.ws.send(JSON.stringify(message));
    }
}

function calculateEloChange(winnerElo, loserElo, K = 32) {
    const expectedWin = 1 / (1 + Math.pow(10, (loserElo - winnerElo) / 400));
    return Math.round(K * (1 - expectedWin));
}

// ==================== MATCHMAKING LOGIC ====================

function findMatch(player) {
    const { playerId, elo, mode } = player;

    // Search for opponent with similar ELO (±200)
    const eloRange = 200;
    const minElo = elo - eloRange;
    const maxElo = elo + eloRange;

    for (let i = 0; i < matchmakingQueue.length; i++) {
        const opponent = matchmakingQueue[i];

        if (opponent.playerId !== playerId &&
            opponent.mode === mode &&
            opponent.elo >= minElo &&
            opponent.elo <= maxElo) {

            // Match found!
            matchmakingQueue.splice(i, 1);
            return opponent;
        }
    }

    return null;
}

function createMatch(player1, player2) {
    const matchId = uuid.v4();

    const match = {
        id: matchId,
        player1: player1,
        player2: player2,
        status: 'ready',
        createdAt: Date.now(),
        mode: player1.mode
    };

    activeMatches.set(matchId, match);

    // Notify both players
    sendToPlayer(player1.playerId, {
        type: 'match_found',
        matchId: matchId,
        opponent: {
            id: player2.playerId,
            username: player2.username,
            elo: player2.elo
        }
    });

    sendToPlayer(player2.playerId, {
        type: 'match_found',
        matchId: matchId,
        opponent: {
            id: player1.playerId,
            username: player1.username,
            elo: player1.elo
        }
    });

    console.log(`🎮 Match créé: ${player1.username} vs ${player2.username} (ELO: ${player1.elo} vs ${player2.elo})`);

    return matchId;
}

// ==================== WEBSOCKET HANDLERS ====================

wss.on('connection', (ws, req) => {
    const clientIp = req.socket.remoteAddress;
    console.log(`🔌 Nouvelle connexion depuis ${clientIp}`);

    let currentPlayerId = null;

    ws.on('message', (message) => {
        try {
            const data = JSON.parse(message);

            switch (data.type) {
                case 'register':
                    handleRegister(ws, data);
                    break;

                case 'join_matchmaking':
                    handleJoinMatchmaking(ws, data);
                    break;

                case 'leave_matchmaking':
                    handleLeaveMatchmaking(ws, data);
                    break;

                case 'match_result':
                    handleMatchResult(ws, data);
                    break;

                case 'create_room':
                    handleCreateRoom(ws, data);
                    break;

                case 'join_room':
                    handleJoinRoom(ws, data);
                    break;

                case 'leave_room':
                    handleLeaveRoom(ws, data);
                    break;

                case 'chat_message':
                    handleChatMessage(ws, data);
                    break;

                case 'ping':
                    ws.send(JSON.stringify({ type: 'pong', timestamp: Date.now() }));
                    break;

                default:
                    console.log('❓ Message inconnu:', data.type);
            }
        } catch (error) {
            console.error('❌ Erreur parsing message:', error);
        }
    });

    ws.on('close', () => {
        if (currentPlayerId) {
            handleDisconnect(currentPlayerId);
        }
        console.log(`🔌 Connexion fermée (${clientIp})`);
    });

    ws.on('error', (error) => {
        console.error('❌ WebSocket error:', error);
    });

    // Handler functions
    function handleRegister(ws, data) {
        const { playerId, username, elo } = data;
        currentPlayerId = playerId;

        connectedPlayers.set(playerId, {
            ws,
            info: {
                playerId,
                username,
                elo: elo || 1000,
                status: 'online',
                connectedAt: Date.now()
            }
        });

        ws.send(JSON.stringify({
            type: 'registered',
            playerId,
            message: 'Connecté au serveur matchmaking'
        }));

        // Broadcast player online
        broadcast({
            type: 'player_online',
            player: { playerId, username, elo: elo || 1000 }
        }, ws);

        console.log(`✅ Joueur enregistré: ${username} (ID: ${playerId})`);
    }

    function handleJoinMatchmaking(ws, data) {
        const { playerId, mode, elo } = data;
        const playerData = connectedPlayers.get(playerId);

        if (!playerData) {
            return ws.send(JSON.stringify({ type: 'error', message: 'Non enregistré' }));
        }

        const playerInfo = {
            playerId,
            username: playerData.info.username,
            elo: elo || playerData.info.elo,
            mode: mode || 'quick',
            timestamp: Date.now()
        };

        // Search for match
        const opponent = findMatch(playerInfo);

        if (opponent) {
            // Match found immediately
            createMatch(playerInfo, opponent);
        } else {
            // Add to queue
            matchmakingQueue.push(playerInfo);

            ws.send(JSON.stringify({
                type: 'searching',
                message: 'Recherche d\'adversaire...',
                queuePosition: matchmakingQueue.length
            }));

            console.log(`🔍 ${playerInfo.username} cherche un match (${mode})`);
        }
    }

    function handleLeaveMatchmaking(ws, data) {
        const { playerId } = data;

        const index = matchmakingQueue.findIndex(p => p.playerId === playerId);
        if (index !== -1) {
            matchmakingQueue.splice(index, 1);
            ws.send(JSON.stringify({
                type: 'left_queue',
                message: 'Sortie de la file d\'attente'
            }));
        }
    }

    function handleMatchResult(ws, data) {
        const { matchId, winnerId, loserId, duration } = data;
        const match = activeMatches.get(matchId);

        if (!match) {
            return ws.send(JSON.stringify({ type: 'error', message: 'Match non trouvé' }));
        }

        const winner = match.player1.playerId === winnerId ? match.player1 : match.player2;
        const loser = match.player1.playerId === loserId ? match.player1 : match.player2;

        const eloChange = calculateEloChange(winner.elo, loser.elo);

        // Update ELOs
        winner.newElo = winner.elo + eloChange;
        loser.newElo = loser.elo - eloChange;

        // Notify both players
        sendToPlayer(winnerId, {
            type: 'match_complete',
            result: 'victory',
            eloChange: `+${eloChange}`,
            newElo: winner.newElo
        });

        sendToPlayer(loserId, {
            type: 'match_complete',
            result: 'defeat',
            eloChange: `-${eloChange}`,
            newElo: loser.newElo
        });

        console.log(`🏆 Match terminé: ${winner.username} bat ${loser.username} (${eloChange} ELO)`);

        // Remove match
        activeMatches.delete(matchId);
    }

    function handleCreateRoom(ws, data) {
        const { playerId, roomName, password, maxPlayers, mode } = data;
        const roomId = uuid.v4();

        const room = {
            id: roomId,
            name: roomName,
            host: playerId,
            password: password || null,
            maxPlayers: maxPlayers || 8,
            mode: mode || '1v1',
            players: [playerId],
            status: 'waiting',
            createdAt: Date.now()
        };

        customRooms.set(roomId, room);

        ws.send(JSON.stringify({
            type: 'room_created',
            roomId,
            room
        }));

        // Broadcast new room
        broadcast({
            type: 'new_room',
            room: {
                id: roomId,
                name: roomName,
                host: playerId,
                currentPlayers: 1,
                maxPlayers,
                mode,
                hasPassword: !!password
            }
        });

        console.log(`🏠 Salle créée: ${roomName} par ${playerId}`);
    }

    function handleJoinRoom(ws, data) {
        const { playerId, roomId, password } = data;
        const room = customRooms.get(roomId);

        if (!room) {
            return ws.send(JSON.stringify({ type: 'error', message: 'Salle non trouvée' }));
        }

        if (room.password && room.password !== password) {
            return ws.send(JSON.stringify({ type: 'error', message: 'Mot de passe incorrect' }));
        }

        if (room.players.length >= room.maxPlayers) {
            return ws.send(JSON.stringify({ type: 'error', message: 'Salle pleine' }));
        }

        room.players.push(playerId);

        ws.send(JSON.stringify({
            type: 'joined_room',
            roomId,
            room
        }));

        // Notify room players
        room.players.forEach(pid => {
            if (pid !== playerId) {
                sendToPlayer(pid, {
                    type: 'player_joined_room',
                    playerId,
                    roomId
                });
            }
        });

        console.log(`✅ ${playerId} a rejoint la salle ${room.name}`);
    }

    function handleLeaveRoom(ws, data) {
        const { playerId, roomId } = data;
        const room = customRooms.get(roomId);

        if (!room) return;

        room.players = room.players.filter(pid => pid !== playerId);

        // If host left, assign new host or delete room
        if (room.host === playerId) {
            if (room.players.length > 0) {
                room.host = room.players[0];
            } else {
                customRooms.delete(roomId);
                broadcast({
                    type: 'room_closed',
                    roomId
                });
                return;
            }
        }

        // Notify room players
        room.players.forEach(pid => {
            sendToPlayer(pid, {
                type: 'player_left_room',
                playerId,
                roomId
            });
        });
    }

    function handleChatMessage(ws, data) {
        const { playerId, roomId, message } = data;
        const room = customRooms.get(roomId);

        if (!room) return;

        // Broadcast to room
        room.players.forEach(pid => {
            sendToPlayer(pid, {
                type: 'chat_message',
                playerId,
                message,
                timestamp: Date.now()
            });
        });
    }

    function handleDisconnect(playerId) {
        // Remove from queue
        const queueIndex = matchmakingQueue.findIndex(p => p.playerId === playerId);
        if (queueIndex !== -1) {
            matchmakingQueue.splice(queueIndex, 1);
        }

        // Remove from connected players
        connectedPlayers.delete(playerId);

        // Broadcast player offline
        broadcast({
            type: 'player_offline',
            playerId
        });

        console.log(`❌ Joueur déconnecté: ${playerId}`);
    }
});

// ==================== SERVER START ====================

server.listen(PORT, () => {
    console.log('╔════════════════════════════════════════════════════════════════╗');
    console.log('║                                                                ║');
    console.log('║       🎯  KOF ULTIMATE ONLINE - MATCHMAKING SERVER             ║');
    console.log('║                     Version 2.0.0                              ║');
    console.log('║                                                                ║');
    console.log('╚════════════════════════════════════════════════════════════════╝');
    console.log('');
    console.log(`✅ Matchmaking Server démarré sur ws://localhost:${PORT}`);
    console.log('');
    console.log('📋 Fonctionnalités:');
    console.log('   • Matchmaking rapide (Quick Match)');
    console.log('   • Matchmaking classé (Ranked)');
    console.log('   • Salles personnalisées');
    console.log('   • Chat en temps réel');
    console.log('   • Système ELO');
    console.log('');
});

// Cleanup on exit
process.on('SIGINT', () => {
    console.log('\n🛑 Arrêt du serveur matchmaking...');
    wss.close(() => {
        console.log('✅ Serveur fermé');
        process.exit(0);
    });
});

module.exports = { server, wss };
