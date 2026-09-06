@echo off
cd /d "%~dp0"
if not exist .env copy .env.example .env
where docker >nul 2>nul
if errorlevel 1 (echo Docker Desktop nao encontrado. Instale o Docker Desktop e tente novamente.&pause&exit /b 1)
docker compose up -d --build
echo.
echo AH TECH Gestao Online iniciado.
echo Acesse: http://localhost:8080
pause
