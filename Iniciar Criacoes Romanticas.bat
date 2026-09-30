@echo off
chcp 65001 >nul
title Criações Românticas - servidor
cd /d "%~dp0"

set PORTA=8501
set ENDERECO=http://localhost:%PORTA%

rem Se o sistema já estiver rodando, só abre o navegador.
powershell -NoProfile -Command "try { if ((Invoke-WebRequest -UseBasicParsing '%ENDERECO%/_stcore/health' -TimeoutSec 2).Content -eq 'ok') { exit 0 } } catch {}; exit 1" >nul 2>&1
if %errorlevel%==0 (
    echo O sistema já está aberto. Abrindo o navegador...
    start "" "%ENDERECO%"
    exit /b 0
)

rem 1) Ambiente Python (criado só na primeira vez).
if not exist ".venv\Scripts\python.exe" (
    echo Preparando o ambiente pela primeira vez. Isso pode levar alguns minutos...
    python -m venv .venv
    if errorlevel 1 (
        echo.
        echo [ERRO] Python não encontrado. Instale em https://www.python.org/downloads/
        echo        marcando a opção "Add Python to PATH", e rode este arquivo de novo.
        pause
        exit /b 1
    )
)

rem 2) Dependências (reinstaladas só quando o requirements.txt mudar).
fc /b requirements.txt ".venv\requirements.instalado" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependências...
    ".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -q -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERRO] Falha ao instalar as dependências. Verifique a conexão com a internet.
        pause
        exit /b 1
    )
    copy /y requirements.txt ".venv\requirements.instalado" >nul
)

rem 3) Abre o navegador assim que o servidor responder (em segundo plano).
start "" /min powershell -NoProfile -WindowStyle Hidden -Command "for ($i = 0; $i -lt 90; $i++) { try { if ((Invoke-WebRequest -UseBasicParsing '%ENDERECO%/_stcore/health' -TimeoutSec 2).Content -eq 'ok') { Start-Process '%ENDERECO%'; break } } catch {}; Start-Sleep -Seconds 1 }"

rem 4) Servidor (fica rodando nesta janela; feche-a para desligar o sistema).
echo.
echo ============================================================
echo   Criações Românticas rodando em %ENDERECO%
echo   Para desligar o sistema, feche esta janela.
echo ============================================================
echo.
".venv\Scripts\python.exe" -m streamlit run app.py --server.port %PORTA% --server.address localhost --server.headless true --browser.gatherUsageStats false

echo.
echo O servidor foi encerrado.
pause
