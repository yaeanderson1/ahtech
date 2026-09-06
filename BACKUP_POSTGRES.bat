@echo off
cd /d "%~dp0"
if not exist backups mkdir backups
for /f "tokens=1-3 delims=/ " %%a in ("%date%") do set D=%%c-%%b-%%a
for /f "tokens=1-2 delims=: " %%a in ("%time%") do set T=%%a%%b
set FILE=backups\ahtech-postgres-%D%-%T%.sql
set FILE=%FILE: =0%
echo Gerando backup PostgreSQL...
docker compose exec -T db pg_dump -U %POSTGRES_USER% -d %POSTGRES_DB% > "%FILE%"
if errorlevel 1 (echo Falha no backup.&pause&exit /b 1)
echo Backup salvo em %FILE%
pause
