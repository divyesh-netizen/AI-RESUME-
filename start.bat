@echo off
echo ===================================================
echo   Starting ResumeIQ AI Resume Screening Platform
echo ===================================================
echo.

start "ResumeIQ Backend (FastAPI)" cmd /k "cd backend && python -m uvicorn main:app --reload --port 8000"
start "ResumeIQ Frontend (Vite React)" cmd /k "cd frontend && npm run dev"

echo.
echo Backend running at: http://127.0.0.1:8000
echo Frontend running at: http://localhost:5173
echo.
echo Press any key to exit this launcher window...
pause > nul
