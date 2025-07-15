# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Lista específica de todos los archivos de datos (imágenes, sonidos, etc.)
added_files = [
    ('assets/images/characters/player/once0.png', 'assets/images/characters/player'),
    ('assets/images/characters/player/once1.png', 'assets/images/characters/player'),
    ('assets/images/characters/player/once2.png', 'assets/images/characters/player'),
    ('assets/images/characters/player/once3.png', 'assets/images/characters/player'),
    ('enemigo.png', '.'),
    ('fondo.png', '.'),
    ('logo.png', '.'),
    ('disparo.wav', '.'),
    ('enemigo_muere.wav', '.'),
    ('daño.wav', '.'),
    ('fondo.mp3', '.'),
    ('puntajes.txt', '.'),
]

a = Analysis(
    ['empezamos.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=['pygame', 'pygame.mixer', 'pygame.font', 'pygame.image', 'pygame.transform'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'matplotlib', 'numpy', 'scipy', 'pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RunOrShoot',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin consola para mejor experiencia de usuario
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Puedes agregar 'logo.ico' si conviertes logo.png a ico
    onefile=True,  # Crear un solo archivo ejecutable
)
