import random
import pygame

# Definimos algunos colores en formato RGB
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

class Universo:
    def __init__(self, filas, columnas, velocidad=.1):
        self.velocidad=velocidad
        self.filas = filas
        self.columnas = columnas
        self.vivos = 0
        self.vivos_anterior = 0
        self.cnt_rep_vivos = 0
        self.estable = False
        self.equilibrio = False
        self.iter = 0
        self.inicializar('vacio')
        print("***Universo creado.")

    def inicializar(self, modo):
        print("***", modo)
        self.estable = False
        self.equilibrio = False
        self.matriz_abuelo = [[0 for j in range(self.columnas)] for i in range(self.filas)]
        self.matriz_anterior = [[0 for j in range(self.columnas)] for i in range(self.filas)]
        self.matriz = [[0 for j in range(self.columnas)] for i in range(self.filas)]
        if modo == "lleno":
            self.matriz = [[1 for j in range(self.columnas)] for i in range(self.filas)]
        elif modo == "columnas":
            for i in range(self.filas):
                if i%2:
                    for j in range(self.columnas):
                        self.matriz[i][j] = 1
        elif modo == "filas":
            for j in range(self.columnas):
                if j%2:
                    for i in range(self.filas):
                        self.matriz[i][j] = 1
        elif modo == "ajedrez":
            for i in range(self.filas):
                for j in range(self.columnas):
                    if (i+j)%2:
                        self.matriz[i][j] = 1
        elif modo == "cros":
            for i in range(self.filas):
                for j in range(self.columnas):
                    if (i+j)<(self.filas+self.columnas)/4 or (i+j)>3*(self.filas+self.columnas)/4:
                        self.matriz[i][j] = 1
        elif modo == "pares":
            for i in range(2, self.filas, 2):
                for j in range(2, self.columnas, 2):
                    self.matriz[i][j] = 1
        elif modo == "rejilla":
            self.matriz = [[1 for j in range(self.columnas)] for i in range(self.filas)]
            for i in range(2, self.filas, 2):
                for j in range(2, self.columnas, 2):
                    self.matriz[i][j] = 0
        elif modo == "random":
            for i in range(self.filas):
                for j in range(self.columnas):
                    self.matriz[i][j] = random.randrange(0, 2)
        vivos = self.contar_vivos()

    def avanzar_generacion(self):
        self.iter += 1
        self.matriz_abuelo = self.matriz_anterior
        self.matriz_anterior = self.matriz
        nuevo_estado = [[0 for j in range(self.columnas)] for i in range(self.filas)]
        self.vivos_anterior = self.vivos
        self.vivos = 0
        for i in range(self.filas):
            for j in range(self.columnas):
                vecinos_vivos = self.contar_vecinos_vivos(i, j)
                # Si la celda est?? viva y tiene 2 o 3 vecinos vivos, sigue viva
                if self.matriz[i][j] == 1 and (vecinos_vivos == 2 or vecinos_vivos == 3):
                    self.vivos += 1
                    nuevo_estado[i][j] = 1
                # Si la celda est?? muerta y tiene exactamente 3 vecinos vivos, resucita
                elif self.matriz[i][j] == 0 and vecinos_vivos == 3:
                    self.vivos += 1
                    nuevo_estado[i][j] = 1
        self.matriz = nuevo_estado
        if self.matriz_abuelo == self.matriz:
            self.cnt_rep_vivos += 1
            if self.cnt_rep_vivos > 100:
                self.equilibrio = True
        self.estable = (self.vivos == self.vivos_anterior)
        return self.vivos

    def contar_vivos(self):
        self.vivos = 0
        self.hay_vivos = False
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.matriz[i][j] == 1:
                    self.vivos += 1
        self.hay_vivos = (self.vivos > 0)
        return self.vivos

    def contar_vecinos_vivos(self, fila, columna):
        contador = 0
        for i in range(fila - 1, fila + 2):
            for j in range(columna - 1, columna + 2):
                # Excluimos la celda actual
                if i == fila and j == columna:
                    continue
                if i >= 0 and i < self.filas and j >= 0 and j < self.columnas:
                    contador += self.matriz[i][j]
        return contador

    def dibujar(self, ventana):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.matriz[i][j] == 0:
                    color = NEGRO
                else:
                    color = BLANCO
                pygame.draw.rect(ventana, color, (i * 5, j * 5, 5, 5))

    def estado(self):
        print(self.iter, self.vivos, self.estable, self.equilibrio, "(", self.cnt_rep_vivos, ")")
