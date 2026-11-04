# KOF-Ultimate-Online — audit de préparation multijoueur

Date de l'audit : 2026-11-04  
Branche de travail : `docs/kofuo-multiplayer-readiness-audit`  
Référence observée : `main` au commit `3883d3723c3f9ac5eeeeb3e9798129efabfd75a3`

## Objet et limites

La priorité est la stabilité locale : le propriétaire signale des crashes fréquents au démarrage et lors du choix d'un personnage ou du lancement d'un combat. La préparation du multijoueur ne commence qu'après un parcours local reproductible et stable. Cet audit prépare le dépôt KOF-Ultimate-Online à un travail de développement assisté par IA pour les tests, l'équilibrage, la stabilité et une future expérience en ligne. Il est fondé sur les fichiers GitHub accessibles à la référence ci-dessus. Il ne prouve pas que le jeu démarre, que les assets externes sont présents, ni qu'une partie en réseau fonctionne.

L'environnement de cette session ne contient pas VM1 ni le bureau Windows de l'utilisateur. Aucun exécutable du jeu, test Windows, test de manette, test LAN ou test en ligne n'a été lancé ici.

## Éléments vérifiés dans le dépôt

| Élément | Observation vérifiable | Conséquence |
|---|---|---|
| Moteur annoncé | `README.md` annonce M.U.G.E.N 1.1.0 Beta 1. | Établir d'abord quel moteur est réellement utilisé par la copie de jeu à tester. |
| Assets volumineux | Le README indique que les personnages (environ 9,7 Go) ne sont pas suivis dans Git. | Un clone seul ne constitue pas une installation jouable complète. L'archive des assets reste à retrouver et à vérifier séparément. |
| Stratégie en ligne documentée | `GUIDE_MULTIJOUEUR.md` propose Ikemen GO, du port-forwarding direct (7500), une alternative Parsec et la désactivation temporaire du pare-feu pour dépanner. | C'est une proposition de guide, pas une preuve de netcode ou d'hébergement effectivement livré. |
| Scripts cités par le guide | Les chemins racine `install_ikemen.py`, `dedicated_server.py` et `test_connection.py` renvoient 404 sur la branche `main` à la date de l'audit. | Les commandes du guide ne sont pas exécutables depuis cette révision sans retrouver ou créer ces fichiers. |
| Test Node | `package.json` définit `npm test` comme un message « No tests configured yet » suivi d'un code de sortie 0. | Un code 0 de cette commande ne valide aucun comportement. |
| Résultat IA archivé | `test_ia_simple_results.json` déclare 744 essais, 668 réussites et 76 crashes (environ 10,2 %). Il ne contient pas de protocole détaillé, de commit testé ni d'environnement. | Signal d'instabilité à investiguer ; ces nombres ne sont pas reproductibles avec les éléments consignés. |\n| Résultat de jouabilité archivé | `test_jouabilite_results.json` enregistre 1 crash sur 5 lancements, puis 14 crashes parmi 124 personnages testés. Le rapport annonce 31 stages, 10 succès et 0 crash, mais ne liste que 10 stages testés. | Corrobore le problème de démarrage et de compatibilité personnage. La couverture des stages est ambiguë ; traiter les nombres comme un ancien relevé, pas comme l'état actuel. |
| Portée des vérificateurs | `verify_game.py` valide surtout la présence de fichiers/dossiers ; il inspecte seulement les 10 premiers personnages pour certains contrôles, puis peut afficher « prêt à être lancé » sans démarrer le moteur. `auto_test_system.py` contrôle des fichiers de configuration et au plus les 50 premiers personnages, pas un combat chargé. | Ces scripts ne peuvent pas certifier la stabilité réelle au démarrage, à la sélection ou au chargement d'un combat. |\n| Test multijoueur Python | `multiplayer_test_system.py` lance les instances séquentiellement dans ses principaux modes, utilise un chemin codé en dur (`D:\\KOF Ultimate Online Online Online`) et lit un journal global fixe (`D:\\KOF Ultimate\\mugen.log`). | Il ne démontre pas des sessions réseau simultanées et peut lire le mauvais journal. Il faut corriger le banc avant de s'appuyer sur ses rapports. |
| Manifeste Python | `requirements.txt` et `pyproject.toml` ne sont pas présents à la racine de cette référence. | Les dépendances et versions des scripts Python ne sont pas verrouillées par un manifeste racine constaté. |

## Décisions à prendre avant d'annoncer un lancement en ligne

1. **Identifier le runtime livré** : M.U.G.E.N existant, portage Ikemen GO, ou séparation entre runtime de combat et services web. Ne pas supposer que les fichiers de configuration de M.U.G.E.N sont compatibles avec Ikemen.
2. **Définir le sens de « massivement multijoueur »** : nombre d'utilisateurs connectés au lobby, nombre de salles simultanées, et nombre de joueurs par combat sont trois objectifs différents.
3. **Séparer les responsabilités** :
   - lobby/comptes/présence/matchmaking comme services de contrôle ;
   - sessions de combat comme processus isolés et versionnés ;
   - distribution et vérification des personnages, stages et règles comme contenu immuable par version.
4. **Choisir le modèle réseau du combat** après vérification des capacités du moteur (par exemple rollback ou simulation déterministe). Ne pas annoncer un serveur dédié de combat tant que le moteur et le protocole ne le prennent pas en charge.
5. **Ne pas désactiver le pare-feu Windows** et ne pas ouvrir un port public pour « dépanner ». Commencer par un test local, puis un réseau de test contrôlé, avec règle minimale, durée limitée et journalisation.

## Séquence de préparation reproductible

### Phase 0 — Inventaire et sauvegardes

- Enregistrer le commit Git, la version du moteur, le matériel, les versions des outils et l'identifiant de l'installation testée.
- Retrouver les 9,7 Go d'assets manquants, vérifier leur provenance, leur arborescence et les empreintes SHA-256 sans les ajouter au dépôt Git.
- Créer un manifeste qui distingue fichiers suivis, assets externes absents et résultats générés.

### Phase 1 — Démarrage hors réseau

- Lancer la copie exacte en mode local sur un poste Windows propre.
- Vérifier le launcher, les configurations, les journaux et la sortie du processus.
- Tester quelques personnages et stages sélectionnés, puis exécuter les outils de validation sans auto-réparation destructive.
- Remplacer les chemins absolus codés en dur par des chemins calculés depuis le dossier du projet et fournir un chemin de log propre à chaque instance.

### Phase 2 — Qualité du banc de tests

- Remplacer le test npm placeholder par des tests qui échouent réellement sur régression.
- Définir une commande de tests Python avec dépendances verrouillées.
- Séparer explicitement : test de démarrage, test de gameplay, test d'intégration réseau et test de charge.
- Pour chaque test, conserver commit, configuration, graine si applicable, journaux, code de sortie et empreintes.

### Phase 3 — Multijoueur contrôlé

- Tester d'abord deux clients sur localhost ou réseau privé, avec versions et empreintes de contenu identiques.
- Mesurer latence, perte, désynchronisation, abandon/reconnexion et fin de session.
- Injecter des délais/pertes réseau déterministes en environnement de test ; ne pas ouvrir de port Internet pour ces essais.
- Valider l'authentification, les limites de débit, l'isolation des salles et les mises à jour du serveur avant toute exposition publique.

### Phase 4 — Charge et préproduction

- Mesurer séparément les utilisateurs de lobby et les parties actives.
- Augmenter la charge par paliers et fixer des critères d'arrêt automatiques CPU, RAM, erreurs, latence et taux de crash.
- Publier uniquement une préproduction fermée, avec procédure de retour arrière et sauvegarde des données.
- N'annoncer une disponibilité publique qu'après des essais multi-clients reproductibles et la validation de la distribution des assets.

## Utilisation des IA et contrôle des changements

Les agents IA peuvent travailler en parallèle sur des tâches indépendantes : inventaire des assets, audit des chemins et configurations, tests de régression, analyse des crashs, équilibrage, documentation et tests du lobby. Chaque tâche doit partir d'une branche distincte, produire des changements limités, citer les fichiers et résultats observés, puis passer les mêmes tests avant revue humaine.

Les IA ne doivent pas présenter comme acquis des tests exécutés seulement à partir de mocks, ni lancer des réparations ou modifier les données de l'installation utilisateur sans sauvegarde vérifiée. Les actions sur l'environnement Windows de VM1 restent à exécuter lorsque cet environnement est effectivement accessible.

## État après cet audit

- Audit de dépôt/documentation : **effectué** pour les fichiers indiqués.
- Code multijoueur modifié : **non**.
- Scripts du guide ajoutés : **non**.
- Test de jeu ou de réseau exécuté : **non**.
- Lancement public prêt : **non démontré**.
- Prochaine action technique prioritaire : dans VM1 accessible, capturer le premier crash reproductible (démarrage/sélection/combat), avec le journal complet, l'identité du personnage/stage et la version du moteur ; récupérer ensuite les assets absents et établir le test de référence. L'audit réseau vient après la stabilité locale.
