# 🎮 KOF Ultimate Launcher - Version Exécutable

## ✅ Compilation réussie!

L'exécutable **KOF Ultimate Launcher.exe** a été créé avec succès!

### 📁 Emplacement
```
D:\KOF Ultimate\dist\KOF Ultimate Launcher.exe
```

### 📊 Informations
- **Taille**: ~37.5 MB
- **Type**: Exécutable Windows autonome (ne nécessite pas Python installé)
- **Date de création**: 15 octobre 2025

## 🚀 Utilisation

### Lancer le jeu
1. Double-cliquez sur **KOF Ultimate Launcher.exe**
2. Choisissez votre mode de jeu:
   - **▶ JOUER** - Lance le jeu principal
   - **🌐 MULTIJOUEUR** - Mode multijoueur
   - **🤖 AI PLAYER** - Mode auto-play avec IA (pour tests)

### Options disponibles
- **Mode Fenêtré** - 800x600 (recommandé pour développement)
- **Plein écran** - Mode de jeu normal
- **🛠 Mode Dev** - Outils de développement
- **⚖ Équilibrage** - Équilibrage des personnages
- **📖 Guide** - Documentation
- **🔄 Vérifier MAJ** - Vérifier les mises à jour

## ⚠️ Important

### Si vous ne pouvez pas jouer normalement (IA joue à votre place)
Le problème vient probablement de:
1. **Le système AI Player est actif** - Fermez la console AI Player si elle est ouverte
2. **Les contrôles sont mappés pour l'IA** - Vérifiez la configuration des touches

### Solution:
Lancez le jeu via **▶ JOUER** et NON via **🤖 AI PLAYER**

## 🎮 Contrôles par défaut (Joueur humain)
```
Mouvement:
  W - Haut
  S - Bas
  A - Gauche
  D - Droite

Attaques:
  J - Coup de poing léger
  K - Coup de poing moyen
  L - Coup de poing fort
  U - Coup de pied léger
  I - Coup de pied moyen
  O - Coup de pied fort

Menu:
  Enter - Start
  Backspace - Select
```

## 📦 Distribution

Pour distribuer le launcher:
1. Copiez le fichier **KOF Ultimate Launcher.exe** n'importe où
2. Assurez-vous qu'il reste dans le dossier du jeu OU
3. Créez un raccourci vers l'exe sur le bureau

### Créer un raccourci sur le bureau
```batch
# Méthode 1: Clic droit > Envoyer vers > Bureau (créer un raccourci)

# Méthode 2: Via PowerShell
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$Home\Desktop\KOF Ultimate.lnk")
$Shortcut.TargetPath = "D:\KOF Ultimate\dist\KOF Ultimate Launcher.exe"
$Shortcut.Save()
```

## 🔧 Recompiler le launcher (si modifications)

Si vous modifiez `launcher.py`:
```bash
cd "D:\KOF Ultimate"
pyinstaller --clean --noconfirm build_launcher.spec
```

Le nouvel exe sera dans `dist/`

## 🎨 Ajouter une icône personnalisée

Pour ajouter une icône au launcher:
1. Créez ou téléchargez un fichier `.ico` (par exemple `kof_icon.ico`)
2. Placez-le dans le dossier du jeu
3. Modifiez `build_launcher.spec`:
```python
icon='kof_icon.ico',  # Ligne 29
```
4. Recompilez avec PyInstaller

## 📝 Notes techniques

### Fichiers inclus dans l'exe
- Python runtime (3.10)
- Tkinter (interface graphique)
- Toutes les dépendances nécessaires
- Le code du launcher

### Ce qui n'est PAS inclus
- Les fichiers du jeu KOF (doivent être dans le même dossier)
- Les configurations (mugen.cfg, etc.)
- Les personnages et stages
- Le système AI Player (nécessite installation séparée)

## 🐛 Dépannage

### Le launcher ne démarre pas
- Vérifiez que vous avez les droits d'exécution
- Essayez de lancer en tant qu'administrateur
- Vérifiez l'antivirus (peut bloquer les exe PyInstaller)

### "Fichier introuvable" lors du lancement du jeu
- L'exe doit être dans le dossier `D:\KOF Ultimate`
- Ou modifier le code pour utiliser des chemins relatifs

### Le launcher est trop volumineux (37 MB)
C'est normal! PyInstaller inclut tout Python. Options:
- Exclure des modules non utilisés dans le .spec
- Utiliser UPX pour compresser (déjà activé)
- Créer une version "onedir" au lieu de "onefile"

## 🎯 Prochaines améliorations possibles

- [ ] Ajouter une icône personnalisée
- [ ] Créer un installateur (NSIS, Inno Setup)
- [ ] Ajouter un splash screen au démarrage
- [ ] Vérification d'intégrité des fichiers
- [ ] Auto-updater intégré
- [ ] Support de plusieurs langues
- [ ] Thèmes personnalisables

## 📞 Support

Si vous rencontrez des problèmes:
1. Vérifiez ce README
2. Consultez les logs dans le dossier du jeu
3. Essayez de lancer `launcher.py` directement avec Python pour voir les erreurs

---

**Créé avec PyInstaller**
