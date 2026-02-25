@echo off
chcp 936 >nul
echo ========================================
echo   GitHub Upload Script
echo ========================================
echo.

cd /d "%~dp0"

echo [1/6] Clearing cached credentials...
git credential-manager reject https://github.com 2>nul
echo.

echo [2/6] Initializing Git repository...
git init
echo.

echo [3/6] Configuring user info...
git config user.email "fonyee@example.com" 2>nul
git config user.name "fonyee" 2>nul
echo.

echo [4/6] Adding all files...
git add .
echo.

echo [5/6] Committing changes...
git commit -m "Initial commit: Auto Macro Tool project"
echo.

echo [6/6] Connecting to remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/fonyee/auto-macro-tool.git
git branch -M main
echo.
echo Pushing to GitHub, please enter username and Token when prompted...
echo Username: fonyee
echo Password: Your Personal Access Token
echo.
git push -u origin main
echo.

echo ========================================
if %errorlevel% == 0 (
    echo   Upload Successful!
) else (
    echo   Upload Failed, please check error messages
)
echo ========================================
pause
