@echo off
echo ===================================================
echo   Starting ResumeIQ Streamlit SaaS Platform
echo ===================================================
echo.

python -m streamlit run app.py --server.port 8501

pause
