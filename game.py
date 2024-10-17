import pygame
import pytmx
import pyscroll
import random
import math

from objects import Ball, Racket
from sound import sound
import tools

class Game :
    def __init__(self, screen, police1, police2) :
        self.screen = screen

        self.etat = False

        self.time_start = pygame.time.get_ticks()

        #création de la balle
        ball_circle = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(ball_circle, (255, 0, 0), (10, 10), 10)
        self.ball = Ball(screen, ball_circle, (540, 360))

        self.ball.a = 1 #coeffcient d'accélération de la balle
        self.time_up_acceleration = 6000

        #création de la raquette du joueur
        racket_rect = pygame.Surface((12, 100))
        pygame.draw.rect(racket_rect, (0, 0, 255), (0, 0, 12, 100))
        self.racket = Racket(screen, racket_rect, (30, 360))

        #création de la raquette de l'adversaire
        racket_ia = pygame.Surface((12, 100))
        pygame.draw.rect(racket_ia, (0, 0, 255), (0, 0, 12, 100))
        self.racket_ia = Racket(screen, racket_ia, (1050, 360))

        #création des obstacles : 
        self.walls = []
        for i in range(random.randint(5, 10)) : 
            self.walls.append(pygame.rect.Rect(random.randint(75, 1005), random.randint(50, 670), random.randint(50, 75), random.randint(50, 75)))

    def set(self) : 
        self.etat = True
        sound.background_music.stop()
        sound.game_music.play(loops=-1)

    def unset(self) :
        self.etat = False
        sound.game_music.stop()
        sound.background_music.play(loops=-1)

    #affichage des éléments de la partie
    def draw(self) : 
        self.ball.draw()
        self.racket.draw()
        self.racket_ia.draw()
        for wall in self.walls :
            pygame.draw.rect(self.screen, (200, 200, 0), wall)

    #applique les actions de la partie
    def apply(self) :

        #applique le mouvement de la balle
        self.ball_acceleration()
        self.ball.apply(self.walls, [self.racket.rect, self.racket_ia.rect])

        #applique le mouvement de la raquette du joueur
        self.racket.apply()

        #applique le mouvement de la raquette de l'adversaire
        self.ia_racket_move()
        self.racket_ia.apply()

    #gère les évènements
    def manage_events(self, event) : 
        #Bouge la raquette du joueur si la touche espace est pressée
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_SPACE:
                self.racket.vy *= -1

    #permet le déplacement automatique de la raquette ennemie (bot)
    def ia_racket_move(self) : 
        #calcule de la future coordonnée y de la balle en x = 1050
        prediction = tools.prediction(self.ball.rect.copy(), self.ball.vx, self.ball.vy, self.ball.a, 1050, self.walls + [self.racket.rect])
        future_ball_coords = prediction[0]
        future_y_coord = tools.find_y(future_ball_coords, 1050, prediction[1], prediction[2])

        #mouvement automatique de la raquette bot en fonction de cette coordonnée y
        if future_y_coord < int((self.racket_ia.rect.top + 2*self.racket_ia.rect.center[1])/3) and self.racket_ia.vy > 0 :
            self.racket_ia.vy *= -1

        elif future_y_coord > int((self.racket_ia.rect.bottom + 2*self.racket_ia.rect.center[1])/3) and self.racket_ia.vy < 0 :
            self.racket_ia.vy *= -1

    #renvoie le temps qui s'est écoulé depuis le début de la partie
    def return_dt(self) :
        return pygame.time.get_ticks() - self.time_start
    
    #renvoie le coefficient d'accélération de la balle en fonction du temps
    def ball_acceleration(self)  :
        if self.ball.vx*self.ball.a < 10 and self.ball.v < 17 : 
            self.ball.a = 1 + (self.return_dt()//self.time_up_acceleration)/10

            if abs(self.racket.a*self.racket.vy) < 12.5 :
                self.racket.a = 1 + (self.return_dt()//self.time_up_acceleration)/10
                self.racket_ia.a = 1 + (self.return_dt()//self.time_up_acceleration)/10

        