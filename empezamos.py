import pygame
import random
import math
import sys
import os

pygame.init()

# Función para obtener la ruta correcta de los recursos
def resource_path(relative_path):
    """ Obtiene la ruta absoluta a un recurso, funciona tanto en desarrollo como en PyInstaller """
    try:
        # PyInstaller crea una carpeta temporal y almacena la ruta en _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


# --- CONFIGURACIONES GENERALES ---
ANCHO = 600
ALTO = 400
NEGRO = (0, 0, 0)
AZUL = (0, 100, 255)
ROJO = (200, 0, 0)
BLANCO = (255, 255, 255)
GRIS = (128, 128, 128)
enemigo_tamaño= 40

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Run or shoot")

fuente_grande = pygame.font.SysFont(None, 60)
fuente_pequeña = pygame.font.SysFont(None, 30)

   
player_img = pygame.image.load(resource_path("assets/images/characters/player/once0.png")).convert_alpha()
player_img = pygame.transform.scale(player_img, (90, 80))
enemigo_img = pygame.image.load(resource_path("enemigo.png")).convert_alpha()
enemigo_img = pygame.transform.scale(enemigo_img,(enemigo_tamaño, enemigo_tamaño))
# Cargar sonidos
sonido_disparo = pygame.mixer.Sound(resource_path("disparo.wav"))
sonido_muere = pygame.mixer.Sound(resource_path("enemigo_muere.wav"))
sonido_danio = pygame.mixer.Sound(resource_path("daño.wav"))
pygame.mixer.music.load(resource_path("fondo.mp3"))
pygame.mixer.music.play(-1)
#mostrar logo
def mostrar_logo():
    logo = pygame.image.load(resource_path("logo.png"))  # asegúrate de que el archivo exista
    logo = pygame.transform.scale(logo, (400, 300))  # ajusta tamaño si es necesario 

    pantalla.fill((0, 0, 0))
    pantalla.blit(logo, (ANCHO // 2 - 200, ALTO // 2 - 150))
    texto = fuente_pequeña.render("Presiona ESPACIO para continuar", True, (255, 255, 255))
    pantalla.blit(texto, (ANCHO // 2 - 170, ALTO - 50))
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                esperando = False

# Función para obtener la ruta del archivo de puntajes
def get_scores_path():
    """ Obtiene la ruta donde guardar los puntajes (carpeta del usuario) """
    try:
        # Intentar usar la carpeta Documents del usuario
        import os
        documents_path = os.path.expanduser("~/Documents")
        if os.path.exists(documents_path):
            return os.path.join(documents_path, "RunOrShoot_puntajes.txt")
    except:
        pass
    # Si no se puede acceder a Documents, usar el directorio actual
    return "puntajes.txt"

# --- FUNCIONES PARA PUNTAJE ---
def guardar_puntaje(puntaje):
    try:
        scores_file = get_scores_path()
        with open(scores_file, "r") as archivo:
            mejor = int(archivo.read().strip() or 0)
    except:
        mejor = 0
    if puntaje > mejor:
        scores_file = get_scores_path()
        with open(scores_file, "w") as archivo:
            archivo.write(str(puntaje))

def obtener_mejor_puntaje():
    try:
        scores_file = get_scores_path()
        with open(scores_file, "r") as archivo:
            contenido = archivo.read().strip()
            return int(contenido) if contenido.isdigit() else 0
    except:
        return 0

# --- FUNCIONES DE PANTALLA ---
def pantalla_inicio():
    pantalla.blit(fondo,(0,0))
   
fondo = pygame.image.load(resource_path("fondo.png")).convert()
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
print(fondo.get_size())  # Esto mostrará el tamaño en la consola

def mostrar_info(puntaje, vidas, mejor_puntaje):
    texto = fuente_pequeña.render(f"Vidas: {vidas}  |  Puntaje: {puntaje}  |  Mejor: {mejor_puntaje}", True, BLANCO)
    pantalla.blit(texto, (10, 10))

# --- PARTIDA PRINCIPAL ---
def jugar():
    personaje_tamaño = 40
    personaje_x = ANCHO // 2
    personaje_y = ALTO // 2
    velocidad = 5
    vidas = 3
    puntaje = 0
    mejor_puntaje = obtener_mejor_puntaje()

    bala_tamaño = 6
    bala_velocidad = 7
    balas = []

    enemigos = []
    enemigo_tamaño = 30
    enemigo_velocidad = 1
    contador = 0

    tiempo_ultimo_golpe = 0
    tiempo_invulnerable = 1000

    obstaculos = [
        pygame.Rect(500, 150, 50, 100),
        pygame.Rect(400, 400, 50, 150),
        pygame.Rect(300, 300, 100, 40)
    ]

    reloj = pygame.time.Clock()
    perdiste = False

    pantalla_inicio()

    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN and not perdiste:
                teclas_disparo = {
                    pygame.K_w: (0, -bala_velocidad),
                    pygame.K_s: (0, bala_velocidad),
                    pygame.K_a: (-bala_velocidad, 0),
                    pygame.K_d: (bala_velocidad, 0),
                    pygame.K_q: (-bala_velocidad, -bala_velocidad),
                    pygame.K_e: (bala_velocidad, -bala_velocidad),
                    pygame.K_z: (-bala_velocidad, bala_velocidad),
                    pygame.K_c: (bala_velocidad, bala_velocidad)
                }
                if evento.key in teclas_disparo:
                    dx, dy = teclas_disparo[evento.key]
                    balas.append({"x": personaje_x, "y": personaje_y, "dx": dx, "dy": dy})
                    sonido_disparo.play()

        if perdiste:
            continue

        # Movimiento del personaje
        pos_anterior = personaje_x, personaje_y
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            personaje_x -= velocidad
        if teclas[pygame.K_RIGHT]:
            personaje_x += velocidad
        if teclas[pygame.K_UP]:
            personaje_y -= velocidad
        if teclas[pygame.K_DOWN]:
            personaje_y += velocidad

        personaje_x = max(0, min(ANCHO - personaje_tamaño, personaje_x))
        personaje_y = max(0, min(ALTO - personaje_tamaño, personaje_y))

        rect_personaje = pygame.Rect(personaje_x, personaje_y, personaje_tamaño, personaje_tamaño)
        for obs in obstaculos:
            if rect_personaje.colliderect(obs):
                personaje_x, personaje_y = pos_anterior
                break

        # Crear enemigos
        contador += 1
        if contador >= 60:
            lado = random.choice(["arriba", "abajo", "izquierda", "derecha"])
            if lado == "arriba":
                x, y = random.randint(0, ANCHO - enemigo_tamaño), -enemigo_tamaño
            elif lado == "abajo":
                x, y = random.randint(0, ANCHO - enemigo_tamaño), ALTO
            elif lado == "izquierda":
                x, y = -enemigo_tamaño, random.randint(0, ALTO - enemigo_tamaño)
            else:
                x, y = ANCHO, random.randint(0, ALTO - enemigo_tamaño)
            enemigos.append({"x": x, "y": y, "vel": enemigo_velocidad})
            contador = 0
            enemigo_velocidad += 0.03

        # Mover enemigos
        for enemigo in enemigos:
            dx = personaje_x - enemigo["x"]
            dy = personaje_y - enemigo["y"]
            distancia = math.hypot(dx, dy)
            if distancia != 0:
                enemigo["x"] += enemigo["vel"] * dx / distancia
                enemigo["y"] += enemigo["vel"] * dy / distancia

        # Mover balas
        for bala in balas:
            bala["x"] += bala["dx"]
            bala["y"] += bala["dy"]

        balas = [b for b in balas if 0 < b["x"] < ANCHO and 0 < b["y"] < ALTO]
        balas = [b for b in balas if not any(pygame.Rect(b["x"], b["y"], bala_tamaño, bala_tamaño).colliderect(obs) for obs in obstaculos)]

        # Colisión bala vs enemigo
        for bala in balas[:]:
            rect_bala= pygame.Rect(bala["x"], bala["y"], bala_tamaño, bala_tamaño)
            for enemigo in enemigos[:]:
                rect_enemigo = pygame.Rect(enemigo["x"], enemigo["y"], enemigo_tamaño, enemigo_tamaño)
                if rect_bala.colliderect(rect_enemigo):
                  balas.remove(bala)
                  sonido_muere.play()
                  enemigos.remove(enemigo)
                  puntaje += 1
                  break

        # Colisión enemigo vs personaje
        tiempo_actual = pygame.time.get_ticks()
        for enemigo in enemigos:
            centro_personaje_x = personaje_x + personaje_tamaño // 2
            centro_personaje_y = personaje_y + personaje_tamaño // 2
            centro_enemigo_x = enemigo["x"] + enemigo_tamaño // 2
            centro_enemigo_y = enemigo["y"] + enemigo_tamaño // 2

            distancia = math.hypot(centro_personaje_x - centro_enemigo_x, centro_personaje_y - centro_enemigo_y)
            if distancia < (personaje_tamaño // 2 + enemigo_tamaño // 2):
                if tiempo_actual - tiempo_ultimo_golpe > tiempo_invulnerable:
                   sonido_danio.play()
                   vidas -= 1
                   tiempo_ultimo_golpe = tiempo_actual #esto es clave 
                   if vidas <=0:
                       guardar_puntaje(puntaje)
                       mejor_puntaje = max(mejor_puntaje, puntaje)
                       perdiste= True
                      
        # Dibujar
        pantalla.blit(fondo,(0,0))
        pantalla.blit(player_img, (personaje_x, personaje_y))
        for enemigo in enemigos:
              pantalla.blit(enemigo_img, (int(enemigo["x"]), int(enemigo["y"])))

        for bala in balas:
            pygame.draw.rect(pantalla, BLANCO, (int(bala["x"]), int(bala["y"]), bala_tamaño, bala_tamaño))

        for obs in obstaculos:
            pygame.draw.rect(pantalla, GRIS, obs)

        mostrar_info(puntaje, vidas, mejor_puntaje)
        pygame.display.flip()
        reloj.tick(60)

        if perdiste:
            pantalla.blit(fondo,(0,0))
            texto = fuente_grande.render("GAME OVER", True, ROJO)
            reiniciar = fuente_pequeña.render("Presiona R para reiniciar o ESC para salir", True, BLANCO)
            pantalla.blit(texto, (ANCHO // 2 - 150, ALTO // 2 - 40))
            pantalla.blit(reiniciar, (ANCHO // 2 - 190, ALTO // 2 + 30))
            pygame.display.flip()
            break

    # Esperar entrada tras perder
        while perdiste:
         for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return "reiniciar"
                elif evento.key == pygame.K_ESCAPE:
                    return False
    
    def mostrar_game_over():
            pantalla.blit(fondo,(0,0))
            texto = fuente_grande.render("GAME OVER", True, ROJO)
            reiniciar = fuente_pequeña.render("Presiona R para reiniciar o ESC para salir", True, BLANCO)
            pantalla.blit(texto, (ANCHO // 2 - 150, ALTO // 2 - 40))
            pantalla.blit(reiniciar, (ANCHO // 2 - 190, ALTO // 2 + 30))
            pygame.display.flip()
            
     
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    return "reiniciar"
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
# --- EJECUCIÓN ---
try:
    mostrar_logo()
    while True:
        resultado = jugar()
        if resultado != "reiniciar":
            break
except KeyboardInterrupt:
    pass
finally:
    pygame.quit()
    sys.exit()
