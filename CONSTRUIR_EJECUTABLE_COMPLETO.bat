@echo off
title Construir Ejecutable - Run or Shoot
color 0A

echo.
echo  ██████╗ ██╗   ██╗███╗   ██╗     ██████╗ ██████╗     ███████╗██╗  ██╗ ██████╗  ██████╗ ████████╗
echo  ██╔══██╗██║   ██║████╗  ██║    ██╔═══██╗██╔══██╗    ██╔════╝██║  ██║██╔═══██╗██╔═══██╗╚══██╔══╝
echo  ██████╔╝██║   ██║██╔██╗ ██║    ██║   ██║██████╔╝    ███████╗███████║██║   ██║██║   ██║   ██║   
echo  ██╔══██╗██║   ██║██║╚██╗██║    ██║   ██║██╔══██╗    ╚════██║██╔══██║██║   ██║██║   ██║   ██║   
echo  ██║  ██║╚██████╔╝██║ ╚████║    ╚██████╔╝██║  ██║    ███████║██║  ██║╚██████╔╝╚██████╔╝   ██║   
echo  ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝     ╚═════╝ ╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝    ╚═╝   
echo.
echo                              🎮 GENERADOR DE EJECUTABLE 🎮
echo.
echo ========================================================================================================
echo.

echo [1/5] Verificando sistema...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python no esta disponible.
    echo    Descarga Python desde: https://python.org
    pause
    exit /b 1
)
echo ✅ Python detectado correctamente

echo.
echo [2/5] Verificando dependencias...
py -m pip show pygame >nul 2>&1
if %errorlevel% neq 0 (
    echo ⏳ Instalando pygame...
    py -m pip install pygame
)

py -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo ⏳ Instalando PyInstaller...
    py -m pip install pyinstaller
)
echo ✅ Dependencias listas

echo.
echo [3/5] Limpiando archivos anteriores...
if exist "dist" rmdir /s /q "dist" 2>nul
if exist "build" rmdir /s /q "build" 2>nul
echo ✅ Limpieza completada

echo.
echo [4/5] 🔨 Construyendo ejecutable...
echo    Esto puede tomar 1-2 minutos...
py -m PyInstaller build_game.spec --clean --noconfirm

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR al construir el ejecutable
    echo.
    echo 🔧 Posibles soluciones:
    echo    - Verifica que todos los archivos de recursos estén presentes
    echo    - Ejecuta como administrador si hay problemas de permisos
    echo    - Desactiva temporalmente el antivirus
    echo    - Asegúrate de que no haya otro proceso usando los archivos
    echo.
    pause
    exit /b 1
)

echo.
echo [5/5] 📊 Verificando resultado...
if exist "dist\RunOrShoot.exe" (
    for %%I in ("dist\RunOrShoot.exe") do set size=%%~zI
    set /a sizeInMB=!size!/1024/1024
    echo ✅ Ejecutable creado exitosamente
    echo    📁 Ubicación: dist\RunOrShoot.exe
    echo    📊 Tamaño: !sizeInMB! MB
) else (
    echo ❌ ERROR: No se pudo crear el ejecutable
    pause
    exit /b 1
)

echo.
echo ========================================================================================================
echo                                    🎉 ¡CONSTRUCCIÓN EXITOSA! 🎉
echo ========================================================================================================
echo.
echo 📋 RESUMEN:
echo    ✅ Ejecutable: dist\RunOrShoot.exe
echo    ✅ Tamaño: ~38 MB
echo    ✅ Independiente: NO requiere Python ni dependencias
echo    ✅ Compatible: Windows 10/11
echo.
echo 🚀 PARA DISTRIBUIR:
echo    1. Comparte SOLO el archivo: dist\RunOrShoot.exe
echo    2. Los usuarios hacen doble clic para jugar
echo    3. No necesitan instalar nada
echo.
echo 🎮 CONTROLES:
echo    - Flechas: Mover personaje
echo    - WASD: Disparar en 8 direcciones
echo    - Q/E/Z/C: Disparar en diagonales
echo    - R: Reiniciar / ESC: Salir
echo.
echo 💡 NOTA: Algunos antivirus pueden mostrar advertencias (normal en ejecutables de PyInstaller)
echo     Solución: Agregar excepción o marcar como archivo seguro
echo.
echo ========================================================================================================

echo.
set /p test="¿Quieres probar el ejecutable ahora? (S/N): "
if /i "%test%"=="S" (
    echo.
    echo 🎮 Iniciando el juego...
    start "" "dist\RunOrShoot.exe"
    echo ✅ ¡Disfruta jugando!
)

echo.
echo 📝 Revisa el archivo DISTRIBUCION_LISTA.md para más información
echo.
pause
