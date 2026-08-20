@echo off
title VKSGroupStream Instant GitHub Sync
color 0A

echo ========================================================
echo   🔄 VKSGroupStream Instant GitHub Auto-Sync Tool
echo ========================================================
echo.

cd /d "C:\Users\vkson\Videos\VKSGroupStream"

set PATH=C:\Users\vkson\AppData\Local\Programs\Git\cmd;%PATH%

echo [1/4] Pulling latest changes from GitHub...
git pull origin main --rebase
echo.

echo [2/4] Adding all local modified and new files...
git add .
echo.

echo [3/4] Creating commit with timestamp...
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
for /f "tokens=1-2 delims=: " %%a in ('time /t') do (set mytime=%%a:%%b)
git commit -m "Update from local PC: %mydate% %mytime%"
echo.

echo [4/4] Pushing to GitHub repository (Kumarvin204/VKSGroupStream)...
git push origin main
echo.

if %ERRORLEVEL% EQU 0 (
    echo ========================================================
    echo   ✅ SUCCESS: Local and GitHub are 100%% IN SYNC!
    echo ========================================================
) else (
    echo ========================================================
    echo   ℹ️ Already up to date or push complete.
    echo ========================================================
)

echo.
echo Press any key to close...
pause > nul
