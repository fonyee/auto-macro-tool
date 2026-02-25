@echo off
chcp 936 >nul
echo ========================================
echo   Delete Files and Push to GitHub
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] Deleting backup_test_files folder...
if exist "backup_test_files" (
    rmdir /s /q "backup_test_files"
    echo [OK] Folder deleted.
) else (
    echo [INFO] Folder not found.
)
echo.

echo [2/4] Deleting cleanup_report.md...
if exist "cleanup_report.md" (
    del /f /q "cleanup_report.md"
    echo [OK] File deleted.
) else (
    echo [INFO] File not found.
)
echo.

echo [3/4] Deleting upload_to_github.bat...
if exist "upload_to_github.bat" (
    del /f /q "upload_to_github.bat"
    echo [OK] File deleted.
) else (
    echo [INFO] File not found.
)
echo.

echo [4/4] Pushing changes to GitHub...
git add .
git commit -m "Remove unnecessary files: backup, report, and upload script"
git push
echo.

echo ========================================
if %errorlevel% == 0 (
    echo   Delete and Push Successful!
) else (
    echo   Operation completed with warnings
)
echo ========================================
pause
