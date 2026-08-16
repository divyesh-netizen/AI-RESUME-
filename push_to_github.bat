@echo off
title Push AI-RESUME to GitHub
echo ==========================================================
echo   Pushing All Folders and Files to GitHub: AI-RESUME-
echo ==========================================================
echo.
echo Connecting to https://github.com/divyesh-netizen/AI-RESUME-...
echo.
echo If a GitHub popup opens, click "Sign in with your browser".
echo.

git push -u origin main

echo.
if %ERRORLEVEL% equ 0 (
    echo ==========================================================
    echo   SUCCESS! All files and subfolders uploaded to GitHub!
    echo ==========================================================
) else (
    echo If it failed, please run: gh auth login --web
)
echo.
pause
