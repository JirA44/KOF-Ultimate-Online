# Diagnostics automatiques KOFUO

## Ce qui est branché

Le bouton « Lancer le Jeu (Solo) » du launcher principal appelle maintenant `DiagnosticRun` avant le démarrage du processus et enregistre un rapport quand le processus termine ou que le lancement échoue. Le collecteur ne modifie ni `select.def`, ni la configuration, ni les fichiers des personnages ; il n'envoie aucune entrée clavier/souris au jeu.

Chaque exécution crée un JSON sous `%LOCALAPPDATA%\KOFUO\diagnostics\reports\` (ou sous `KOFUO_DIAGNOSTICS_LOCAL_DIR` si cette variable est définie). Si un nouveau `mugen.log` est créé ou modifié pendant cette exécution, une copie brute est conservée localement dans `raw_logs\`. Les anciens journaux ne sont jamais effacés.

Le rapport de partage contient un identifiant, l'heure UTC, le code de sortie, la durée, les empreintes SHA-256 du binaire et du journal, des marqueurs techniques et un petit extrait expurgé. Il ne contient pas le chemin d'installation, le journal brut, une capture d'écran, une mémoire de processus, un nom d'utilisateur ou une adresse IP. Une durée courte est signalée comme indice, pas classée comme crash certain.

## Livraison locale à Supa via un dossier partagé

La VM peut rester sans accès Internet. Configure un dossier partagé VirtualBox qui pointe vers un dossier de l'hôte, par exemple `C:\KOFUOReports`, avec le nom `KOFUOReports`.

- Dans la VM Windows, définir `KOFUO_DIAGNOSTICS_OUTBOX=\\VBOXSVR\KOFUOReports`.
- Sur l'hôte où tourne Supa, définir `SUPA_KOFUO_DIAGNOSTICS_DIR=C:\KOFUOReports` avant de démarrer l'API.
- Garder `KOFUO_DIAGNOSTICS_LOCAL_DIR` sur le disque de la VM pour que les journaux bruts restent locaux.

La PR compagnon Supa ajoute une lecture locale en `GET /games/kofuo/diagnostics` et `GET /games/kofuo/diagnostics/{report_id}`. Elle ne lance pas un modèle automatiquement, ne modifie pas les rapports et ne crée pas d'accès réseau supplémentaire. L'API actuelle de Supa écoute sur `127.0.0.1` ; ce dispositif utilise le dossier partagé au lieu d'exposer le port de Supa à la VM.

## Mise en service et limites

- Les variables d'environnement et le partage VirtualBox doivent être définis dans les environnements hôte/VM ; cette session ne peut pas accéder au bureau Windows pour les configurer.
- Le launcher principal est le seul point de lancement instrumenté dans cette PR. Le processus est surveillé à sa sortie; un processus bloqué n'est pas encore détecté. Les autres anciens launchers ou un lancement direct de l'exécutable ne passent pas encore par le collecteur.
- Le rapport paraît après la fermeture du processus. Le collecteur ne sait pas observer un crash interne qui laisse le processus bloqué ; il n'interroge pas l'Observateur d'événements Windows.
- Le rapporteur historique `COMPLETE_ERROR_REPORTER.py` n'est pas appelé : il supprime `mugen.log`, remplace `select.def` pour ses essais et termine le jeu après trois secondes. Ne pas le lancer sur l'installation de référence.
- Aucun crash actuel n'a été reproduit depuis cette session ; l'intégration Windows/VM et la réception par Supa restent à vérifier dès que VM1 sera pilotable.

## Paramètres

| Variable | Usage | Défaut |
|---|---|---|
| `KOFUO_GAME_DIR` | Répertoire du jeu si différent du dossier du launcher | Dossier du launcher |
| `KOFUO_DIAGNOSTICS_LOCAL_DIR` | Rapports et journaux bruts locaux de la VM | Répertoire utilisateur KOFUO |
| `KOFUO_DIAGNOSTICS_OUTBOX` | Dossier partagé où écrire uniquement le JSON expurgé | Livraison Supa désactivée |
| `SUPA_KOFUO_DIAGNOSTICS_DIR` | Dossier partagé lu par l'API Supa | Lecture API désactivée |
