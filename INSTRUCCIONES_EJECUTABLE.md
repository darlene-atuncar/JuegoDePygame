# INSTRUCCIONES PARA CREAR EJECUTABLE

## Requisitos previos:
1. Tener Python instalado en tu sistema
2. Tener pygame instalado (`pip install pygame`)

## Pasos para crear el ejecutable:

### Opción 1: Usar el script automático (RECOMENDADO)
1. Haz doble clic en `build_executable.bat` o `CONSTRUIR_EJECUTABLE_COMPLETO.bat`
2. Espera a que termine el proceso
3. El ejecutable estará en la carpeta `dist`

### Opción 2: Manual
1. Instalar PyInstaller:
   ```
   pip install pyinstaller
   ```

2. Ejecutar la construcción:
   ```
   pyinstaller build_game.spec
   ```

3. El ejecutable estará en `dist/RunOrShoot.exe`

## Distribución:
- Para distribuir el juego, comparte toda la carpeta `dist`
- El archivo `RunOrShoot.exe` necesita estar junto con los demás archivos
- Los usuarios NO necesitan tener Python instalado para jugar

## Notas:
- El proceso puede tomar varios minutos
- El ejecutable será considerablemente más grande que el código fuente
- Si tienes problemas, asegúrate de que todos los archivos de recursos (imágenes, sonidos) estén presentes

## Controles del juego:
- Flechas: Mover personaje
- WASD: Disparar en 8 direcciones
- Q/E/Z/C: Disparar en diagonales
- R: Reiniciar después de Game Over
- ESC: Salir
