@echo off
echo ========================================
echo    CONSTRUYENDO EJECUTABLE DEL JUEGO
echo ========================================
echo.

echo Verificando que Python este disponible...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python no esta disponible. Por favor instala Python desde python.org
    pause
    exit /b 1
)

echo Verificando que PyInstaller este instalado...
py -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller no esta instalado. Instalando...
    py -m pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Error al instalar PyInstaller.
        pause
        exit /b 1
    )
)

echo Verificando que pygame este instalado...
py -m pip show pygame >nul 2>&1
if %errorlevel% neq 0 (
    echo pygame no esta instalado. Instalando...
    py -m pip install pygame
    if %errorlevel% neq 0 (
        echo Error al instalar pygame.
        pause
        exit /b 1
    )
)

echo.
echo Limpiando directorios anteriores...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo.
echo Construyendo el ejecutable...
py -m PyInstaller build_game.spec --clean --noconfirm

if %errorlevel% neq 0 (
    echo Error al construir el ejecutable.
    echo.
    echo Posibles soluciones:
    echo - Verifica que todos los archivos de recursos esten presentes
    echo - Ejecuta como administrador si hay problemas de permisos
    echo - Revisa que no haya antivirus bloqueando el proceso
    pause
    exit /b 1
)

echo.
echo ========================================
echo    CONSTRUCCION COMPLETADA!
echo ========================================
echo.
echo El ejecutable se encuentra en: dist\RunOrShoot.exe
echo.
echo IMPORTANTE: Este es un archivo COMPLETAMENTE INDEPENDIENTE
echo - NO requiere Python instalado para ejecutarse
echo - NO requiere pygame ni otras dependencias
echo - Puede ejecutarse en cualquier PC Windows
echo - Comparte solo el archivo RunOrShoot.exe
echo.
echo Tamaño aproximado: 50-100 MB (normal para ejecutables de juegos)
echo.
pause
