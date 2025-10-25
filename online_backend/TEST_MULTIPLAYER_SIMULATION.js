#!/usr/bin/env node
/**
 * TEST SIMULATION MULTIJOUEUR - KOF Ultimate Online
 * Simule de vrais joueurs utilisant la plateforme comme Battle.net
 */

const WebSocket = require('ws');
const fetch = require('node-fetch');

// Configuration
const API_URL = 'http://localhost:3100';
const WS_URL = 'ws://localhost:3101';
const NUM_PLAYERS = 10; // Nombre de joueurs virtuels
const TEST_DURATION = 300000; // 5 minutes de test

// Noms de joueurs réalistes
const PLAYER_NAMES = [
    'DragonSlayer', 'ShadowNinja', 'ThunderKing', 'IceQueen', 'PhoenixFire',
    'StormBreaker', 'NightHawk', 'BlazeMaster', 'CrystalBlade', 'VoidWalker',
    'DarkKnight', 'LightBringer', 'FrostWolf', 'FireDragon', 'WindRunner',
    'EarthShaker', 'StarGazer', 'MoonDancer', 'SunWarrior', 'OceanTide'
];

class VirtualPlayer {
    constructor(username, elo = 1000) {
        this.username = username;
        this.elo = elo;
        this.token = null;
        this.playerId = null;
        this.ws = null;
        this.inMatch = false;
        this.matchHistory = [];
        this.connectionStatus = 'disconnected';
    }

    log(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const colors = {
            info: '\x1b[36m',
            success: '\x1b[32m',
            error: '\x1b[31m',
            warning: '\x1b[33m',
            match: '\x1b[35m'
        };
        const color = colors[type] || colors.info;
        console.log(`${color}[${timestamp}] [${this.username}] ${message}\x1b[0m`);
    }

    async register() {
        try {
            const response = await fetch(`${API_URL}/api/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: this.username,
                    email: `${this.username.toLowerCase()}@kof-ultimate.com`,
                    password: 'password123'
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.token = data.token;
                this.playerId = data.player.id;
                this.log('✅ Compte créé avec succès', 'success');
                return true;
            } else {
                // Si déjà existant, on tente de se connecter
                return await this.login();
            }
        } catch (error) {
            this.log(`❌ Erreur inscription: ${error.message}`, 'error');
            return false;
        }
    }

    async login() {
        try {
            const response = await fetch(`${API_URL}/api/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    username: this.username,
                    password: 'password123'
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.token = data.token;
                this.playerId = data.player.id;
                this.elo = data.player.elo || 1000;
                this.log('✅ Connexion réussie', 'success');
                return true;
            } else {
                this.log(`❌ Erreur connexion: ${data.error}`, 'error');
                return false;
            }
        } catch (error) {
            this.log(`❌ Erreur login: ${error.message}`, 'error');
            return false;
        }
    }

    async getProfile() {
        try {
            const response = await fetch(`${API_URL}/api/players/profile`, {
                headers: { 'Authorization': `Bearer ${this.token}` }
            });

            const data = await response.json();
            if (response.ok) {
                this.log(`📊 Profil: ELO ${data.player.elo} | Victoires ${data.stats.wins} | Défaites ${data.stats.losses}`, 'info');
                return data;
            }
        } catch (error) {
            this.log(`⚠️ Erreur récupération profil: ${error.message}`, 'warning');
        }
    }

    connectMatchmaking() {
        return new Promise((resolve, reject) => {
            try {
                this.ws = new WebSocket(WS_URL);

                this.ws.on('open', () => {
                    this.connectionStatus = 'connected';
                    this.log('🔌 Connecté au matchmaking', 'success');

                    // S'enregistrer dans le matchmaking
                    this.ws.send(JSON.stringify({
                        type: 'register',
                        playerId: this.playerId,
                        username: this.username,
                        elo: this.elo
                    }));

                    resolve();
                });

                this.ws.on('message', (data) => {
                    try {
                        const message = JSON.parse(data);
                        this.handleMatchmakingMessage(message);
                    } catch (error) {
                        this.log(`⚠️ Message invalide: ${error.message}`, 'warning');
                    }
                });

                this.ws.on('error', (error) => {
                    this.log(`❌ Erreur WebSocket: ${error.message}`, 'error');
                    this.connectionStatus = 'error';
                });

                this.ws.on('close', () => {
                    this.log('🔌 Déconnecté du matchmaking', 'warning');
                    this.connectionStatus = 'disconnected';
                });

                setTimeout(() => {
                    if (this.connectionStatus !== 'connected') {
                        reject(new Error('Timeout connexion matchmaking'));
                    }
                }, 10000);

            } catch (error) {
                reject(error);
            }
        });
    }

    handleMatchmakingMessage(message) {
        switch (message.type) {
            case 'registered':
                this.log('✅ Enregistré dans le matchmaking', 'success');
                break;

            case 'queue_joined':
                this.log(`🎮 En file d'attente (${message.position}/${message.total} joueurs)`, 'info');
                break;

            case 'match_found':
                this.inMatch = true;
                this.log(`🎯 MATCH TROUVÉ! vs ${message.opponent.username} (ELO ${message.opponent.elo})`, 'match');
                this.log(`   Match ID: ${message.matchId}`, 'match');

                // Simuler le chargement du match
                setTimeout(() => this.acceptMatch(message.matchId), 2000);
                break;

            case 'match_accepted':
                this.log('✅ Match accepté, lancement du jeu...', 'success');
                break;

            case 'match_started':
                this.log('🎮 COMBAT COMMENCÉ!', 'match');

                // Simuler une partie (30-60 secondes)
                const duration = 30000 + Math.random() * 30000;
                setTimeout(() => this.endMatch(message.matchId), duration);
                break;

            case 'match_result':
                const result = message.result === 'win' ? '🏆 VICTOIRE' : '💀 DÉFAITE';
                const eloChange = message.eloChange > 0 ? `+${message.eloChange}` : message.eloChange;
                this.log(`${result}! ELO: ${this.elo} → ${message.newElo} (${eloChange})`, 'match');
                this.elo = message.newElo;
                this.inMatch = false;

                this.matchHistory.push({
                    result: message.result,
                    eloChange: message.eloChange,
                    opponent: message.opponent
                });

                // Rejoindre la queue après un délai
                setTimeout(() => this.joinQueue(), 5000);
                break;

            case 'player_count':
                if (message.count > 1) {
                    this.log(`👥 ${message.count} joueurs en ligne`, 'info');
                }
                break;

            case 'error':
                this.log(`❌ Erreur: ${message.message}`, 'error');
                break;
        }
    }

    joinQueue(mode = 'ranked') {
        if (this.inMatch || this.connectionStatus !== 'connected') {
            return;
        }

        this.log(`🎯 Recherche de match (${mode})...`, 'info');

        this.ws.send(JSON.stringify({
            type: 'join_queue',
            playerId: this.playerId,
            mode: mode
        }));
    }

    acceptMatch(matchId) {
        this.log('✅ Acceptation du match...', 'success');

        this.ws.send(JSON.stringify({
            type: 'accept_match',
            playerId: this.playerId,
            matchId: matchId
        }));
    }

    endMatch(matchId) {
        // Simuler un résultat aléatoire (50/50)
        const won = Math.random() > 0.5;

        this.log(`📊 Fin du combat - ${won ? 'Victoire' : 'Défaite'}`, 'info');

        this.ws.send(JSON.stringify({
            type: 'match_complete',
            playerId: this.playerId,
            matchId: matchId,
            result: won ? 'win' : 'loss'
        }));
    }

    leaveQueue() {
        if (this.ws && this.connectionStatus === 'connected') {
            this.ws.send(JSON.stringify({
                type: 'leave_queue',
                playerId: this.playerId
            }));
        }
    }

    disconnect() {
        this.leaveQueue();

        if (this.ws) {
            this.ws.close();
        }

        this.log('👋 Déconnecté', 'info');
    }

    async getLeaderboard() {
        try {
            const response = await fetch(`${API_URL}/api/leaderboard?limit=10`);
            const data = await response.json();

            if (response.ok) {
                this.log('🏆 TOP 10 LEADERBOARD:', 'info');
                data.leaderboard.forEach((player, index) => {
                    this.log(`   ${index + 1}. ${player.display_name} - ${player.elo} ELO`, 'info');
                });
            }
        } catch (error) {
            this.log(`⚠️ Erreur leaderboard: ${error.message}`, 'warning');
        }
    }
}

class MultiplayerTestSimulation {
    constructor() {
        this.players = [];
        this.stats = {
            totalMatches: 0,
            totalConnections: 0,
            errors: 0,
            startTime: Date.now()
        };
    }

    log(message, type = 'info') {
        const timestamp = new Date().toLocaleTimeString();
        const colors = {
            info: '\x1b[36m',
            success: '\x1b[32m',
            error: '\x1b[31m',
            warning: '\x1b[33m',
            header: '\x1b[95m\x1b[1m'
        };
        const color = colors[type] || colors.info;
        console.log(`${color}[${timestamp}] [SYSTEM] ${message}\x1b[0m`);
    }

    async checkServers() {
        this.log('🔍 Vérification des serveurs...', 'info');

        try {
            // Test API
            const apiResponse = await fetch(`${API_URL}/api/health`);
            if (apiResponse.ok) {
                this.log('✅ API Server OK (port 3100)', 'success');
            } else {
                throw new Error('API Server non disponible');
            }
        } catch (error) {
            this.log('❌ API Server non disponible - Lancement requis', 'error');
            return false;
        }

        return true;
    }

    async createPlayers(count) {
        this.log(`👥 Création de ${count} joueurs virtuels...`, 'info');

        for (let i = 0; i < count; i++) {
            const username = PLAYER_NAMES[i % PLAYER_NAMES.length] + (i > PLAYER_NAMES.length - 1 ? i : '');
            const baseElo = 800 + Math.floor(Math.random() * 400); // ELO entre 800 et 1200

            const player = new VirtualPlayer(username, baseElo);
            this.players.push(player);
        }

        this.log(`✅ ${count} joueurs créés`, 'success');
    }

    async initializePlayers() {
        this.log('🔐 Inscription/Connexion des joueurs...', 'info');

        const promises = this.players.map(async (player) => {
            const success = await player.register();
            if (success) {
                this.stats.totalConnections++;
            } else {
                this.stats.errors++;
            }
        });

        await Promise.all(promises);

        this.log(`✅ ${this.stats.totalConnections}/${this.players.length} joueurs connectés`, 'success');
    }

    async connectAllToMatchmaking() {
        this.log('🎮 Connexion au matchmaking...', 'info');

        const promises = this.players.map(async (player) => {
            try {
                await player.connectMatchmaking();
                await new Promise(resolve => setTimeout(resolve, 500)); // Délai entre connexions
            } catch (error) {
                player.log(`❌ Erreur connexion matchmaking: ${error.message}`, 'error');
                this.stats.errors++;
            }
        });

        await Promise.all(promises);

        const connected = this.players.filter(p => p.connectionStatus === 'connected').length;
        this.log(`✅ ${connected}/${this.players.length} joueurs en matchmaking`, 'success');
    }

    async startMatchmaking() {
        this.log('🎯 Démarrage du matchmaking pour tous les joueurs...', 'info');

        // Tous les joueurs rejoignent la queue
        this.players.forEach(player => {
            if (player.connectionStatus === 'connected') {
                player.joinQueue('ranked');
            }
        });
    }

    async simulateActivity() {
        this.log(`⏱️ Simulation d'activité pendant ${TEST_DURATION / 1000}s...`, 'info');

        // Activité aléatoire des joueurs
        const activityInterval = setInterval(() => {
            this.players.forEach(player => {
                if (player.connectionStatus === 'connected' && !player.inMatch) {
                    // 30% de chance de rejoindre la queue si pas déjà dedans
                    if (Math.random() > 0.7) {
                        player.joinQueue('ranked');
                    }
                }
            });
        }, 10000); // Toutes les 10 secondes

        // Attendre la durée du test
        await new Promise(resolve => setTimeout(resolve, TEST_DURATION));

        clearInterval(activityInterval);
    }

    async generateReport() {
        this.log('', 'info');
        this.log('=' .repeat(80), 'header');
        this.log('📊 RAPPORT FINAL - SIMULATION MULTIJOUEUR', 'header');
        this.log('='.repeat(80), 'header');

        const duration = (Date.now() - this.stats.startTime) / 1000;
        const totalMatches = this.players.reduce((sum, p) => sum + p.matchHistory.length, 0);

        this.log(`\n⏱️ Durée du test: ${Math.floor(duration / 60)}min ${Math.floor(duration % 60)}s`, 'info');
        this.log(`👥 Joueurs créés: ${this.players.length}`, 'info');
        this.log(`🔌 Connexions réussies: ${this.stats.totalConnections}`, 'success');
        this.log(`🎮 Total de matchs joués: ${totalMatches}`, 'success');
        this.log(`❌ Erreurs détectées: ${this.stats.errors}`, this.stats.errors > 0 ? 'error' : 'success');

        this.log('\n🏆 TOP 5 JOUEURS:', 'info');
        const sortedPlayers = [...this.players].sort((a, b) => b.elo - a.elo).slice(0, 5);
        sortedPlayers.forEach((player, index) => {
            const wins = player.matchHistory.filter(m => m.result === 'win').length;
            const losses = player.matchHistory.filter(m => m.result === 'loss').length;
            this.log(`   ${index + 1}. ${player.username} - ${player.elo} ELO (${wins}W/${losses}L)`, 'info');
        });

        this.log('\n📈 STATISTIQUES PAR JOUEUR:', 'info');
        this.players.forEach(player => {
            if (player.matchHistory.length > 0) {
                const wins = player.matchHistory.filter(m => m.result === 'win').length;
                const losses = player.matchHistory.filter(m => m.result === 'loss').length;
                const winRate = (wins / (wins + losses) * 100).toFixed(1);
                this.log(`   • ${player.username}: ${player.matchHistory.length} matchs | ${winRate}% WR | ${player.elo} ELO`, 'info');
            }
        });

        this.log('\n' + '='.repeat(80), 'header');

        if (this.stats.errors === 0 && totalMatches > 0) {
            this.log('✅ SYSTÈME MULTIJOUEUR 100% FONCTIONNEL!', 'success');
        } else if (totalMatches > 0) {
            this.log('⚠️ SYSTÈME FONCTIONNEL AVEC QUELQUES ERREURS', 'warning');
        } else {
            this.log('❌ SYSTÈME NON FONCTIONNEL - AUCUN MATCH JOUÉ', 'error');
        }

        this.log('='.repeat(80), 'header');
    }

    async cleanup() {
        this.log('🧹 Nettoyage...', 'info');

        this.players.forEach(player => {
            player.disconnect();
        });

        await new Promise(resolve => setTimeout(resolve, 2000));

        this.log('✅ Nettoyage terminé', 'success');
    }

    async run() {
        console.log('\n' + '='.repeat(80));
        console.log('\x1b[95m\x1b[1m🎮 TEST SIMULATION MULTIJOUEUR - KOF ULTIMATE ONLINE\x1b[0m');
        console.log('='.repeat(80) + '\n');

        try {
            // 1. Vérifier que les serveurs sont lancés
            const serversOk = await this.checkServers();
            if (!serversOk) {
                this.log('❌ Lancez d\'abord les serveurs avec: npm run start:servers', 'error');
                return;
            }

            // 2. Créer les joueurs virtuels
            await this.createPlayers(NUM_PLAYERS);

            // 3. Inscrire/connecter les joueurs
            await this.initializePlayers();

            // 4. Connecter au matchmaking
            await this.connectAllToMatchmaking();

            // 5. Démarrer le matchmaking
            await this.startMatchmaking();

            // 6. Simuler l'activité
            await this.simulateActivity();

            // 7. Générer le rapport
            await this.generateReport();

            // 8. Nettoyage
            await this.cleanup();

        } catch (error) {
            this.log(`❌ Erreur critique: ${error.message}`, 'error');
            console.error(error);
        }

        this.log('\n✅ Test terminé!', 'success');
        process.exit(0);
    }
}

// Lancement
if (require.main === module) {
    const simulation = new MultiplayerTestSimulation();
    simulation.run().catch(error => {
        console.error('Erreur fatale:', error);
        process.exit(1);
    });
}

module.exports = MultiplayerTestSimulation;
