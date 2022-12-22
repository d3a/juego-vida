import sys
import time
import pygame

from universo import Universo

# Inicializamos pygame
pygame.init()

# Creamos una ventana de tamaño 800x600
ventana = pygame.display.set_mode((1500, 1000))

def leer_teclado():
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            return event.key
    return 'none'

def pausa():
    a=leer_teclado()
    while a == 'none':
        a=leer_teclado()

def esperar_teclado():
    a=leer_teclado()
    while a == 'none':
        a=leer_teclado()
    return a
    
def lanzaUniverso(ventana,modo,velocidad=.2):
    print("Lanzando en modo: ", modo)
    universo = Universo(300, 200, velocidad)
    universo.inicializar(modo)
    universo.dibujar(ventana)
    pygame.display.flip()

    universo.estado()
    keypressed = False
    while not keypressed and universo.vivos > 0:
        universo.avanzar_generacion()
        if universo.iter % 25 == 0:
            universo.estado()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                keypressed = True
        universo.dibujar(ventana)
        pygame.display.flip()
        time.sleep(universo.velocidad)
    
    universo.estado()
    if keypressed:
        print("  Cancelado en ", str(universo.iter), " iteraciones: ", universo.vivos)
        exit()
    elif universo.estable:
        print("  Estabilizado en ", str(universo.iter), " iteraciones: ", universo.vivos)
    elif universo.equilibrio:
        print("  Equilibrado en ", str(universo.iter), " iteraciones: ", universo.vivos)
    elif universo.vivos == 0:
        print("  Todos muertos tras ", str(universo.iter), " iteraciones.")
        exit()
    pausa()

# Creamos una instancia del juego de la vida
lanzaUniverso(ventana,'cros', .1)

