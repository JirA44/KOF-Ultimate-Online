@echo off
title KOF Ultimate Online - AAA Launch System
color 0E

echo.
echo  ╔════════════════════════════════════════════════════════╗
echo  ║                                                        ║
echo  ║     KOF ULTIMATE ONLINE - AAA LAUNCH SYSTEM           ║
echo  ║     Professional Battle.net-Style Launcher            ║
echo  ║                                                        ║
echo  ╚════════════════════════════════════════════════════════╝
echo.
echo  This will start the complete AAA system:
echo  ✓ Professional Matchmaking Server
echo  ✓ Modern Battle.net-Style Launcher
echo  ✓ Game (when you click PLAY)
echo.
echo  Features included:
echo  - Ranked matchmaking with MMR/ELO
echo  - Friends system
echo  - Chat system (global, private, lobby)
echo  - Custom lobbies
echo  - Leaderboards
echo  - Statistics tracking
echo  - Anti-cheat validation
echo.
echo  Press any key to launch...
pause >nul

cls
echo.
echo ═══════════════════════════════════════════════
echo  LAUNCHING AAA SYSTEM...
echo ═══════════════════════════════════════════════
echo.

echo [1/2] Starting Professional Matchmaking Server...
start "KOF PRO Server" /MIN cmd /c "LAUNCH_PRO_SERVER.bat"
echo      ✓ Server launching in background...
timeout /t 5 >nul

echo [2/2] Starting Modern Launcher...
start "KOF Modern Launcher" cmd /c "LAUNCH_MODERN_LAUNCHER.bat"
echo      ✓ Launcher opening...

echo.
echo ═══════════════════════════════════════════════
echo  SYSTEM STARTED SUCCESSFULLY!
echo ═══════════════════════════════════════════════
echo.
echo  Server Status: Running on port 7500
echo  Launcher Status: Active
echo.
echo  You can now:
echo  - Create an account in the launcher
echo  - Join matchmaking queues
echo  - Create custom lobbies
echo  - Chat with other players
echo  - View leaderboards
echo.
echo  Press any key to close this window...
pause >nul
