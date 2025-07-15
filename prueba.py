import pygame

pygame.init()

pantalla = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Ventana de prueba")

pantalla.fill((0, 0, 0))  # Fondo negro
pygame.draw.rect(pantalla, (0, 100, 255), (280, 180, 40, 40))  # Personaje

pygame.display.flip()

# Esperar 3 segundos para ver la ventana
pygame.time.wait(3000)


pygame.quit()