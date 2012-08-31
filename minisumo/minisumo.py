#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Minisumo.py a simple minisumo tournament management software
Copyright (C) 2012 Lucas Chiesa

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
El programa necesita python-pygame (debian/ubuntu)

Se corre con python cronometro.py.
Teclas:
 * ESC: mostrar ganador
 * q: salir del programa
 * s: stop o 0x00 en el puerto serie
 * p: play o 0x01 en el puerto serie
 * d: stop pero descartar el tiempo.
 * r: reset

Al finalizar escribe en un archivo de texto (tiempos.txt) en modo escritura los tiempos
medidos de las carreras y tambien los imprime por pantalla.
"""

import sys, pygame, datetime, serial, os, math
import time

import cars

print cars.cars

# Se configura el tamaño de la ventana.
size = width, height = 800, 600


class Cronometro(object):
    DOWN, UP = range(2)

    def __init__(self, back, game, init_time=5, max_time=3*60):
        self.back = back
        self.game = game
        self.paused = False
        self.started = datetime.timedelta(0)
        self.init_time = datetime.timedelta(seconds=init_time)
        self.max_time = datetime.timedelta(seconds=max_time)
        self.last_time_shown = self.init_time
        self.running = False
        self.font = pygame.font.SysFont("Monospace", 100, bold=True)
        self.estado = self.DOWN
        self.render(self.init_time)
        self.back.blit(self.text, self.textpos)

    def reset(self):
        self.started = datetime.datetime.now()
        self.render(datetime.timedelta(0))

    def start(self):
        self.estado = self.DOWN
        self.running = True
        self.started = datetime.datetime.now()

    def pause(self):
        self.paused = not self.paused

    def stop(self):
        if self.running:
            self.running = False
            self.estado = self.DOWN
            self.render(self.last_time_shown)
        else:
            if self.estado == self.DOWN:
                self.render(self.init_time)
            else:
                self.render(self.max_time)

    def update(self):
        if self.paused:
            datetime_paused = (datetime.datetime.now() - self.last_time_shown)
            timedelta_paused = datetime_paused - self.started
            self.started += timedelta_paused

        if self.running and not self.paused:
            now = datetime.datetime.now()
            if self.estado == self.DOWN:
                left = self.init_time - (now - self.started)
                self.render(left)
                if left <= datetime.timedelta(0):
                    self.reset()
                    w = self.game.get_world()
                    w.estado = COMPITIENDO
                    self.estado = self.UP
            if self.estado == self.UP:
                tiempo_pasado = now - self.started
                self.render(tiempo_pasado)
                if tiempo_pasado >= self.max_time:
                    w = self.game.get_world()
                    w.estado = TERMINADO
                    #self.estado = self.DOWN
                    self.running = False
                    self.stop()
        else:
            self.render()

    def render(self, timedelta=None):
        if timedelta is not None:
            elapsed_txt = clockformat(timedelta)
            self.text = self.font.render(elapsed_txt, 1, (10, 10, 10))
            self.last_time_shown = timedelta
        self.textpos = self.text.get_rect(centerx=width/2, centery=height*5.0/6.0)
        self.back.blit(self.text, self.textpos)

def clockformat(timedelta):
    return "%02d:%02d.%02d" % (timedelta.seconds /60,
                        timedelta.seconds % 60,
                        int(str(timedelta.microseconds)[0:2]))

IDLE, CUENTA_INICIAL, COMPITIENDO, TERMINADO = range(4)

class World(object):
    def __init__(self, back, cronometro):
        self.crono = cronometro
        self.back = back
        self.ayuda = "1,2: autos - q,w: aumentan puntos - a,s: bajan puntos - z: aumenta asalto - x: baja asalto | p: comienza, o: termina, l: reiniciar cronometro, BACKSPACE = reset total"
        self.estado = IDLE
        self.font = pygame.font.SysFont("Monospace", 85, bold=True)
        self.font_chica = pygame.font.SysFont("Monospace", 14,bold=False)
        self.auto1 = str(cars.cars[0])
        self.auto1_puntaje = 0
        self.auto2 = str(cars.cars[0])
        self.auto2_puntaje = 0
        self.asalto_num = 0

    def load_image(self, name):
        fullname = os.path.join('.', name)
        image = pygame.image.load(fullname)
        image = image.convert_alpha()
        return image, image.get_rect()

    def render(self):
        if self.estado == IDLE:
            self.back.fill((255,255,255)) #Blanco
            self.crono.update()
        elif self.estado == CUENTA_INICIAL:
            self.back.fill((230, 230, 133)) #Amarillo
            self.crono.update()
        elif self.estado == COMPITIENDO:
            self.back.fill((0, 255, 0)) #Verde
            self.crono.update()
        elif self.estado == TERMINADO:
            self.back.fill((0, 255, 250)) #No se que es
            self.crono.update()

        banner, banner_rect = self.load_image("logo-club-banner.png")
        self.back.blit(banner, (102,0))
        asalto = self.font.render("Asalto", 1, (200, 10, 10))
        asalto_num = self.font.render(str(self.asalto_num), 1, (200, 10, 10))
        auto1 = self.font.render(self.auto1, 1, (10, 10, 10))
        auto1_puntaje = self.font.render(str(self.auto1_puntaje), 1, (10, 10, 10))
        auto2 = self.font.render(self.auto2, 1, (10, 10, 10))
        auto2_puntaje = self.font.render(str(self.auto2_puntaje), 1, (10, 10, 10))
        self.back.blit(asalto, asalto.get_rect(centerx=width/2, centery=int(height*.5/6.0)))
        self.back.blit(asalto_num, asalto_num.get_rect(centerx=width/2, centery=int(height*1.5/6.0)))
        self.back.blit(auto1, auto1.get_rect(centerx=width/4, centery=int(height*2.5/6.0)))
        self.back.blit(auto1_puntaje, auto1_puntaje.get_rect(centerx=width/4, centery=int(height*3.5/6.0)))
        self.back.blit(auto2, auto2.get_rect(centerx=3.0*width/4, centery=int(height*2.5/6.0)))
        self.back.blit(auto2_puntaje, auto2_puntaje.get_rect(centerx=3.0*width/4, centery=int(height*3.5/6.0)))

        # Imprimo el texto de ayuda
        ayuda = self.font_chica.render(self.ayuda[0:self.ayuda.find('|')], 1, (100,100,100))
        self.back.blit(ayuda, ayuda.get_rect(centerx=width/2, centery=int(height*5.7/6.0)))
        ayuda = self.font_chica.render(self.ayuda[self.ayuda.find('|')+1:], 1, (100,100,100))
        self.back.blit(ayuda, ayuda.get_rect(centerx=width/2, centery=int(height*5.9/6.0)))


class Game():
    
    def change_car (self, indice):
        indice = (indice + 1)%len(cars.cars)
        auto = str(cars.cars[indice][0:9])
        return indice, auto

    def get_world (self):
        return self.world

    def __init__ (self):
        pygame.init()
        
        pygame.mouse.set_visible(True)
        
        pygame.font.init()
        colors = {"red":(255, 0, 0), "green":(0,255,0), "black":(0,0,0), "white":(255,255,255)}
        screen = pygame.display.set_mode(size, pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
        pygame.display.set_caption("Minisumo")
        #pygame.mouse.set_visible(False)
        ck = pygame.time.Clock()
        background = pygame.Surface(screen.get_size())
        background = background.convert()

        cronometro = Cronometro(background, self)
        world = World(background, cronometro)
        self.world = world

        indice_auto1 = 0
        indice_auto2 = 0

        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or \
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                             indice_auto1, world.auto1 = self.change_car(indice_auto1)
                             world.render()
                    elif event.key == pygame.K_2:
                             indice_auto2, world.auto2 = self.change_car(indice_auto2)
                             world.render()
                    elif event.key ==  pygame.K_l:
                        cronometro.stop()
                        cronometro.stop() # Si, tienen que ser dos.
                        world.estado = IDLE
                        world.render()
                    elif event.key == pygame.K_p:
                        cronometro.start()
                        world.estado = CUENTA_INICIAL
                    elif event.key == pygame.K_o:
                        cronometro.stop()
                        world.estado = TERMINADO
                    elif event.key == pygame.K_q:
                        world.auto1_puntaje += 1
                    elif event.key == pygame.K_a:
                        world.auto1_puntaje -= 1
                    elif event.key == pygame.K_w:
                        world.auto2_puntaje += 1
                    elif event.key == pygame.K_s:
                        world.auto2_puntaje -= 1
                    elif event.key == pygame.K_z:
                        world.asalto_num += 1
                    elif event.key == pygame.K_x:
                        world.asalto_num -= 1
                    elif event.key == pygame.K_BACKSPACE:
                        cronometro.stop()
                        cronometro.stop() # Si, tienen que ser dos.
                        world.estado = IDLE
                        world.auto1_puntaje = 0
                        world.auto2_puntaje = 0
                        world.asalto_num = 0
                        world.render()
                # Preguntamos si paso algo con el mouse
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x = event.pos[0]
                        y = event.pos[1]
                        if x > 40 and x < 470 and y > 260 and y < 530:
                            world.auto1_puntaje += 1
                        elif x > 560 and x < 1000 and y > 260 and y < 530:
                            world.auto2_puntaje += 1
                        elif x > 320 and x < 710 and y > 10 and y < 240:
                            world.asalto_num += 1
                        elif x > 315 and x < 690 and y > 590 and y < 690:
                            if world.estado == COMPITIENDO:
                                cronometro.stop()
                                world.estado = TERMINADO
                            elif world.estado == TERMINADO:
                                cronometro.stop()
                                cronometro.stop() # Si, tienen que ser dos.
                                world.estado = IDLE
                                world.render()
                            elif world.estado == IDLE:
                                cronometro.start()
                                world.estado = CUENTA_INICIAL

            world.render()
            screen.blit(background, (0, 0))
            pygame.display.flip()


if __name__ == '__main__':
    g = Game()

