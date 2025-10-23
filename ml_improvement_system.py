"""
Système d'Amélioration Continue par Machine Learning - KOF Ultimate Online
Analyse les matchs et améliore automatiquement les joueurs virtuels
"""

import json
import os
import time
from datetime import datetime, timedelta
from collections import defaultdict
import random
import math

class MLImprovementSystem:
    """Système d'apprentissage automatique pour améliorer les joueurs virtuels"""

    def __init__(self):
        self.learning_sessions = []
        self.global_meta = {
            'total_learning_cycles': 0,
            'average_skill_improvement': 0.0,
            'best_performers': [],
            'fastest_learners': [],
            'optimal_strategies': {}
        }

    def analyze_match_patterns(self, players):
        """Analyse les patterns de matchs pour identifier les stratégies gagnantes"""
        print("\n🧠 Analyse des patterns de matchs...")

        strategies_performance = defaultdict(lambda: {'wins': 0, 'losses': 0, 'total': 0})

        for player in players:
            playstyle = player.profile['preferences']['playstyle']
            stats = player.profile['stats']

            strategies_performance[playstyle]['wins'] += stats['wins']
            strategies_performance[playstyle]['losses'] += stats['losses']
            strategies_performance[playstyle]['total'] += stats['total_matches']

        # Calculer les winrates par stratégie
        strategy_rankings = []
        for strategy, perf in strategies_performance.items():
            if perf['total'] > 0:
                winrate = perf['wins'] / perf['total']
                strategy_rankings.append({
                    'strategy': strategy,
                    'winrate': winrate,
                    'matches': perf['total']
                })

        strategy_rankings.sort(key=lambda x: x['winrate'], reverse=True)

        print("\n📈 Performance par stratégie:")
        for rank in strategy_rankings[:5]:
            print(f"   {rank['strategy']:15} - WR: {rank['winrate']*100:.1f}% ({rank['matches']} matchs)")

        self.global_meta['optimal_strategies'] = strategy_rankings
        return strategy_rankings

    def identify_top_performers(self, players, top_n=5):
        """Identifie les meilleurs joueurs pour analyse"""
        sorted_players = sorted(
            players,
            key=lambda p: p.profile['stats']['ranking_points'],
            reverse=True
        )

        top_performers = []
        for player in sorted_players[:top_n]:
            top_performers.append({
                'name': player.name,
                'mmr': player.profile['stats']['ranking_points'],
                'winrate': player.profile['stats']['winrate'],
                'brain': player.profile['ai_brain'],
                'playstyle': player.profile['preferences']['playstyle']
            })

        print(f"\n🏆 Top {top_n} performers identifiés:")
        for i, perf in enumerate(top_performers, 1):
            print(f"   {i}. {perf['name']} - MMR: {perf['mmr']:.0f} - WR: {perf['winrate']*100:.1f}%")

        self.global_meta['best_performers'] = top_performers
        return top_performers

    def calculate_optimal_brain_parameters(self, top_performers):
        """Calcule les paramètres cérébraux optimaux à partir des top performers"""
        if not top_performers:
            return None

        optimal_brain = {
            'aggression': 0,
            'defense': 0,
            'combo_skill': 0,
            'reaction_time': 0,
            'adaptation': 0
        }

        # Moyenne pondérée par le MMR
        total_weight = sum(p['mmr'] for p in top_performers)

        for performer in top_performers:
            weight = performer['mmr'] / total_weight
            brain = performer['brain']

            for key in optimal_brain.keys():
                optimal_brain[key] += brain[key] * weight

        print(f"\n🧬 Paramètres cérébraux optimaux calculés:")
        for key, value in optimal_brain.items():
            print(f"   {key:15}: {value:.3f}")

        return optimal_brain

    def improve_weaker_players(self, players, optimal_brain, improvement_rate=0.3):
        """Améliore les joueurs les plus faibles en se basant sur les meilleurs"""
        print(f"\n📊 Amélioration des joueurs faibles (taux: {improvement_rate*100:.0f}%)...")

        # Trier par MMR
        sorted_players = sorted(players, key=lambda p: p.profile['stats']['ranking_points'])

        # Améliorer le bottom 30%
        num_to_improve = int(len(sorted_players) * 0.3)
        improved_count = 0

        for player in sorted_players[:num_to_improve]:
            old_skill = player.calculate_skill_score()
            brain = player.profile['ai_brain']

            # Appliquer l'amélioration
            for key in optimal_brain.keys():
                if key == 'reaction_time':
                    # Pour reaction_time, plus bas = mieux
                    target = optimal_brain[key]
                    brain[key] = brain[key] * (1 - improvement_rate) + target * improvement_rate
                else:
                    target = optimal_brain[key]
                    brain[key] = brain[key] * (1 - improvement_rate) + target * improvement_rate

            new_skill = player.calculate_skill_score()
            improvement = ((new_skill - old_skill) / old_skill) * 100

            print(f"   ✓ {player.name}: {old_skill:.3f} -> {new_skill:.3f} (+{improvement:.1f}%)")
            improved_count += 1

        print(f"\n✅ {improved_count} joueurs améliorés!")
        return improved_count

    def transfer_knowledge(self, source_player, target_player, transfer_rate=0.2):
        """Transfère les connaissances d'un joueur expert à un joueur novice"""
        source_brain = source_player.profile['ai_brain']
        target_brain = target_player.profile['ai_brain']

        for key in source_brain.keys():
            if key == 'learning_rate':
                continue  # Ne pas transférer le taux d'apprentissage

            source_value = source_brain[key]
            target_value = target_brain[key]

            # Transfert graduel
            new_value = target_value * (1 - transfer_rate) + source_value * transfer_rate
            target_brain[key] = new_value

        print(f"🔄 Connaissance transférée: {source_player.name} -> {target_player.name}")

    def adaptive_learning_rate_adjustment(self, players):
        """Ajuste le taux d'apprentissage basé sur la performance"""
        print("\n⚙️  Ajustement adaptatif des taux d'apprentissage...")

        for player in players:
            stats = player.profile['stats']
            brain = player.profile['ai_brain']

            # Si le joueur stagne (peu de matchs ou mauvais winrate), augmenter learning_rate
            if stats['total_matches'] > 10:
                if stats['winrate'] < 0.4:
                    # Performance faible -> apprentissage plus agressif
                    brain['learning_rate'] = min(0.1, brain['learning_rate'] * 1.2)
                    print(f"   📈 {player.name}: learning_rate augmenté à {brain['learning_rate']:.4f}")

                elif stats['winrate'] > 0.6:
                    # Performance élevée -> apprentissage plus conservateur
                    brain['learning_rate'] = max(0.01, brain['learning_rate'] * 0.9)
                    print(f"   📉 {player.name}: learning_rate réduit à {brain['learning_rate']:.4f}")

    def evolutionary_algorithm(self, players, generation_size=5):
        """Applique un algorithme évolutionnaire pour créer de meilleurs joueurs"""
        print(f"\n🧬 Algorithme évolutionnaire (génération de {generation_size} nouveaux joueurs)...")

        # Sélectionner les meilleurs joueurs comme "parents"
        sorted_players = sorted(
            players,
            key=lambda p: p.profile['stats']['ranking_points'],
            reverse=True
        )

        parents = sorted_players[:generation_size]

        # Créer de nouveaux joueurs en combinant les cerveaux des parents
        for i in range(generation_size):
            parent1 = random.choice(parents)
            parent2 = random.choice(parents)

            print(f"   🧬 Hybride: {parent1.name} x {parent2.name}")

            # Crossover: mélanger les cerveaux
            new_brain = {}
            for key in parent1.profile['ai_brain'].keys():
                # 50% de chance de prendre de chaque parent
                if random.random() < 0.5:
                    new_brain[key] = parent1.profile['ai_brain'][key]
                else:
                    new_brain[key] = parent2.profile['ai_brain'][key]

            # Mutation: ajouter un peu de randomness
            for key in new_brain.keys():
                if random.random() < 0.2:  # 20% de chance de mutation
                    mutation = random.uniform(-0.1, 0.1)
                    new_brain[key] = max(0.1, min(1.0, new_brain[key] + mutation))

            print(f"      -> Nouveau cerveau créé avec mutations")

    def run_learning_cycle(self, players):
        """Exécute un cycle complet d'apprentissage"""
        print("\n" + "="*60)
        print("🎓 CYCLE D'APPRENTISSAGE AUTOMATIQUE")
        print("="*60)

        start_time = time.time()

        # 1. Analyser les patterns
        strategy_rankings = self.analyze_match_patterns(players)

        # 2. Identifier les top performers
        top_performers = self.identify_top_performers(players, top_n=5)

        # 3. Calculer les paramètres optimaux
        optimal_brain = self.calculate_optimal_brain_parameters(top_performers)

        # 4. Améliorer les joueurs faibles
        if optimal_brain:
            improved_count = self.improve_weaker_players(players, optimal_brain, improvement_rate=0.25)

        # 5. Ajuster les learning rates
        self.adaptive_learning_rate_adjustment(players)

        # 6. Transfert de connaissance aléatoire
        if len(players) >= 2:
            for _ in range(5):  # 5 transferts aléatoires
                expert = random.choice(top_performers) if top_performers else None
                novice = random.choice([p for p in players if p.profile['stats']['ranking_points'] < 1000])

                if expert and novice:
                    expert_player = next((p for p in players if p.name == expert['name']), None)
                    if expert_player:
                        self.transfer_knowledge(expert_player, novice, transfer_rate=0.15)

        # 7. Enregistrer la session
        duration = time.time() - start_time

        session = {
            'cycle_number': self.global_meta['total_learning_cycles'] + 1,
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'players_improved': improved_count if optimal_brain else 0,
            'top_strategy': strategy_rankings[0]['strategy'] if strategy_rankings else 'unknown',
            'avg_mmr': sum(p.profile['stats']['ranking_points'] for p in players) / len(players)
        }

        self.learning_sessions.append(session)
        self.global_meta['total_learning_cycles'] += 1

        print(f"\n✅ Cycle d'apprentissage terminé en {duration:.2f}s")
        print("="*60 + "\n")

        return session

    def continuous_improvement_loop(self, players, interval_minutes=30):
        """Boucle d'amélioration continue"""
        print(f"\n🔄 Démarrage de l'amélioration continue (tous les {interval_minutes} min)...\n")

        while True:
            try:
                # Attendre l'intervalle
                time.sleep(interval_minutes * 60)

                # Exécuter un cycle d'apprentissage
                self.run_learning_cycle(players)

                # Sauvegarder les profils
                for player in players:
                    player.save_profile()

                # Sauvegarder les métadonnées
                self.save_meta()

            except KeyboardInterrupt:
                print("\n🛑 Arrêt de l'amélioration continue...")
                break
            except Exception as e:
                print(f"❌ Erreur dans le cycle d'apprentissage: {e}")

    def save_meta(self):
        """Sauvegarde les métadonnées du système ML"""
        data = {
            'global_meta': self.global_meta,
            'learning_sessions': self.learning_sessions[-50:],  # Garder les 50 dernières sessions
            'last_update': datetime.now().isoformat()
        }

        with open('ml_system_meta.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_meta(self):
        """Charge les métadonnées sauvegardées"""
        try:
            with open('ml_system_meta.json', 'r', encoding='utf-8') as f:
                data = json.load(f)

            self.global_meta = data.get('global_meta', self.global_meta)
            self.learning_sessions = data.get('learning_sessions', [])

            print(f"✅ Métadonnées ML chargées : {len(self.learning_sessions)} sessions")
        except FileNotFoundError:
            print("ℹ️  Nouveau système ML, aucune métadonnée trouvée")

    def generate_improvement_report(self):
        """Génère un rapport d'amélioration"""
        if not self.learning_sessions:
            return "Aucune session d'apprentissage enregistrée"

        report = []
        report.append("\n" + "="*60)
        report.append("📊 RAPPORT D'AMÉLIORATION CONTINUE")
        report.append("="*60)

        report.append(f"\nTotal de cycles: {self.global_meta['total_learning_cycles']}")

        if self.learning_sessions:
            latest = self.learning_sessions[-1]
            report.append(f"Dernier cycle:   {latest['timestamp']}")
            report.append(f"Joueurs améliorés: {latest['players_improved']}")
            report.append(f"Stratégie dominante: {latest['top_strategy']}")
            report.append(f"MMR moyen: {latest['avg_mmr']:.0f}")

        if self.global_meta.get('optimal_strategies'):
            report.append(f"\n🎯 Stratégies optimales:")
            for strat in self.global_meta['optimal_strategies'][:3]:
                report.append(f"   - {strat['strategy']}: {strat['winrate']*100:.1f}% WR")

        report.append("="*60)

        return "\n".join(report)


def main():
    """Programme principal"""
    print("\n" + "="*60)
    print("  SYSTÈME D'AMÉLIORATION CONTINUE ML")
    print("="*60)

    # Note: Ce script nécessite que les joueurs virtuels soient déjà créés
    print("\nℹ️  Ce système doit être lancé EN MÊME TEMPS que les joueurs virtuels")
    print("ℹ️  Il analyse et améliore automatiquement les joueurs toutes les 30 min")


if __name__ == "__main__":
    main()
