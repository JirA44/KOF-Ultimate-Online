"""
Live Reporter - KOF Ultimate Online
Génère des rapports toutes les 5 minutes sur l'activité du système
"""

import json
import time
import os
from datetime import datetime
from collections import defaultdict

class LiveReporter:
    def __init__(self):
        self.report_count = 0
        self.previous_total_matches = 0

    def load_data(self):
        """Charge les données depuis les fichiers JSON"""
        data = {
            'matchmaking': None,
            'ml': None,
            'error': None
        }

        try:
            if os.path.exists('matchmaking_state.json'):
                with open('matchmaking_state.json', 'r', encoding='utf-8') as f:
                    data['matchmaking'] = json.load(f)
        except Exception as e:
            data['error'] = f"Erreur matchmaking: {e}"

        try:
            if os.path.exists('ml_system_meta.json'):
                with open('ml_system_meta.json', 'r', encoding='utf-8') as f:
                    data['ml'] = json.load(f)
        except Exception as e:
            pass  # ML data est optionnel

        return data

    def generate_report(self):
        """Génère un rapport complet"""
        self.report_count += 1
        data = self.load_data()

        # Header
        report = []
        report.append("\n" + "="*70)
        report.append(f"📊 RAPPORT #{self.report_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("="*70)

        # Vérifier si les données existent
        if data['error']:
            report.append(f"\n⚠️  {data['error']}")
            report.append("\n💡 Le système démarre probablement... Attendre 10-15 secondes.")
            report.append("="*70 + "\n")
            return "\n".join(report)

        matchmaking = data['matchmaking']
        ml = data['ml']

        if not matchmaking:
            report.append("\n⏳ Aucune donnée disponible. Le système démarre...")
            report.append("="*70 + "\n")
            return "\n".join(report)

        # Stats globales
        report.append("\n📈 STATISTIQUES GLOBALES")
        report.append("-"*70)

        elo_ratings = matchmaking.get('elo_ratings', {})
        player_stats = matchmaking.get('player_stats', {})
        match_history = matchmaking.get('match_history', [])

        total_players = len(elo_ratings)
        total_matches = len(match_history)
        new_matches = total_matches - self.previous_total_matches

        report.append(f"👥 Joueurs enregistrés:    {total_players}")
        report.append(f"⚔️  Total des matchs:       {total_matches}")
        report.append(f"🆕 Nouveaux matchs (5 min): {new_matches}")

        if total_players > 0:
            avg_elo = sum(elo_ratings.values()) / total_players
            report.append(f"📊 ELO moyen:              {avg_elo:.0f}")

        self.previous_total_matches = total_matches

        # Top 5 Joueurs
        report.append("\n🏆 TOP 5 JOUEURS")
        report.append("-"*70)

        if elo_ratings:
            sorted_players = sorted(
                elo_ratings.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]

            medals = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']

            for i, (player_id, elo) in enumerate(sorted_players):
                stats = player_stats.get(player_id, {})
                wins = stats.get('wins', 0)
                losses = stats.get('losses', 0)
                winrate = stats.get('winrate', 0) * 100
                skill = stats.get('skill_level', 'Unknown')

                report.append(
                    f"{medals[i]} {player_id[:20]:20} | "
                    f"ELO: {elo:4.0f} | "
                    f"W/L: {wins:2}/{losses:2} | "
                    f"WR: {winrate:5.1f}% | "
                    f"{skill}"
                )
        else:
            report.append("   Aucun joueur encore enregistré")

        # Bottom 5 (ceux qui ont besoin d'amélioration)
        report.append("\n📉 BOTTOM 5 (En progression)")
        report.append("-"*70)

        if len(elo_ratings) >= 5:
            bottom_players = sorted(
                elo_ratings.items(),
                key=lambda x: x[1]
            )[:5]

            for i, (player_id, elo) in enumerate(bottom_players, 1):
                stats = player_stats.get(player_id, {})
                wins = stats.get('wins', 0)
                losses = stats.get('losses', 0)
                winrate = stats.get('winrate', 0) * 100

                report.append(
                    f"{i:2}. {player_id[:20]:20} | "
                    f"ELO: {elo:4.0f} | "
                    f"W/L: {wins:2}/{losses:2} | "
                    f"WR: {winrate:5.1f}%"
                )

        # Matchs récents (derniers 5)
        report.append("\n⚔️  MATCHS RÉCENTS (5 derniers)")
        report.append("-"*70)

        if match_history:
            recent_matches = match_history[-5:][::-1]  # 5 derniers, inversés

            for match in recent_matches:
                player1 = match.get('player1', 'Unknown')
                player2 = match.get('player2', 'Unknown')
                winner = match.get('winner', 'Unknown')
                p1_elo = match.get('player1_elo', 0)
                p2_elo = match.get('player2_elo', 0)

                winner_symbol = "🏆" if winner == player1 else "💀"
                loser_symbol = "💀" if winner == player1 else "🏆"

                report.append(
                    f"   {winner_symbol} {player1[:15]:15} ({p1_elo:4.0f}) vs "
                    f"{loser_symbol} {player2[:15]:15} ({p2_elo:4.0f})"
                )
        else:
            report.append("   Aucun match encore joué")

        # Stats ML
        if ml and ml.get('global_meta'):
            report.append("\n🧠 MACHINE LEARNING")
            report.append("-"*70)

            meta = ml['global_meta']
            cycles = meta.get('total_learning_cycles', 0)
            report.append(f"🔄 Cycles d'apprentissage: {cycles}")

            optimal_strategies = meta.get('optimal_strategies', [])
            if optimal_strategies:
                report.append("\n🎯 Stratégies optimales:")
                for i, strat in enumerate(optimal_strategies[:3], 1):
                    strategy = strat.get('strategy', 'Unknown')
                    winrate = strat.get('winrate', 0) * 100
                    matches = strat.get('matches', 0)
                    report.append(f"   {i}. {strategy:15} - {winrate:5.1f}% WR ({matches} matchs)")

        # Distribution par niveau
        report.append("\n📊 DISTRIBUTION PAR NIVEAU")
        report.append("-"*70)

        skill_distribution = defaultdict(int)
        for stats in player_stats.values():
            skill = stats.get('skill_level', 'Unknown')
            skill_distribution[skill] += 1

        skill_order = ['Master', 'Expert', 'Advanced', 'Intermediate', 'Beginner']
        for skill in skill_order:
            count = skill_distribution.get(skill, 0)
            if count > 0:
                bar = "█" * count
                report.append(f"   {skill:15} ({count:2}): {bar}")

        # Activité (matchs par minute)
        if new_matches > 0:
            matches_per_minute = new_matches / 5
            report.append("\n⏱️  ACTIVITÉ")
            report.append("-"*70)
            report.append(f"   Matchs/minute: {matches_per_minute:.1f}")
            report.append(f"   Estimation matchs/heure: {matches_per_minute * 60:.0f}")

        # Footer
        report.append("\n" + "="*70)
        report.append(f"⏰ Prochain rapport dans 5 minutes...")
        report.append("="*70 + "\n")

        return "\n".join(report)

    def run(self):
        """Lance la boucle de reporting"""
        print("\n" + "="*70)
        print("🎬 LIVE REPORTER - KOF ULTIMATE ONLINE")
        print("="*70)
        print("\n📊 Génération de rapports toutes les 5 minutes")
        print("⏰ Premier rapport dans quelques secondes...")
        print("\n⚠️  Appuyez sur Ctrl+C pour arrêter\n")
        print("="*70 + "\n")

        try:
            while True:
                # Générer et afficher le rapport
                report = self.generate_report()
                print(report)

                # Attendre 5 minutes (300 secondes)
                time.sleep(300)

        except KeyboardInterrupt:
            print("\n\n🛑 Arrêt du Live Reporter")
            print("✅ Rapports générés: " + str(self.report_count))
            print("\n👋 Au revoir!\n")


def main():
    """Programme principal"""
    reporter = LiveReporter()
    reporter.run()


if __name__ == "__main__":
    main()
