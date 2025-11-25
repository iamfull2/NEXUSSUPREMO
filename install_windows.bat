@echo off
REM ═══════════════════════════════════════════════════════════════════
REM  NEXUS SUPREME v1.0 - Script de Instalação Rápida (Windows)
REM ═══════════════════════════════════════════════════════════════════

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║         🔥 NEXUS SUPREME v1.0 - Instalação Automática 🔥    ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não está instalado ou não está no PATH
    echo.
    echo Faça download de: https://www.python.org/downloads/
    echo Certifique-se de marcar "Add Python to PATH"
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Instala dependências
echo ⏳ Instalando dependências necessárias...
echo.

pip install --upgrade pip
pip install selenium>=4.0.0 webdriver-manager>=3.8.0 colorama>=0.4.6

if errorlevel 1 (
    echo.
    echo ❌ ERRO ao instalar dependências
    pause
    exit /b 1
)

echo.
echo ✅ Todas as dependências foram instaladas com sucesso!
echo.

REM Verifica se o script principal existe
if not exist "NEXUS_SUPREME.py" (
    echo ⚠️  AVISO: NEXUS_SUPREME.py não encontrado na pasta atual
    echo.
    echo Certifique-se de que o arquivo está na mesma pasta deste instalador
    pause
    exit /b 1
)

echo ✅ NEXUS_SUPREME.py encontrado
echo.

REM Abre o sistema
echo 🚀 Iniciando NEXUS SUPREME...
echo.
timeout /t 2 /nobreak

python NEXUS_SUPREME.py

pause
