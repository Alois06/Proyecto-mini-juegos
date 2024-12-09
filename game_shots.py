import pygame
import random
import math

from sound import sound
from objects import PlayerShooter, Obstacle
import tools

#classe de la partie normale
class Game :
    def __init__(self, screen, police1, police2, police3, police4) :
        self.screen = screen

        self.etat = False

        self.game_over_etat = False

        #polices
        self.police1 = police1
        self.police2 = police2
        self.police3 = police3
        self.police4 = police4

        #variables de temps
        self.time_start = pygame.time.get_ticks()
        self.time_start_game_over = None
        self.start_countdown_delay = 5000
        self.end_countdown_delay = 10000

        #image de fond d'écran
        self.background = pygame.image.load("assets/background_désert.PNG")
        self.background = pygame.transform.scale(self.background, (1080, 720))

        #joueurs
        self.player1 = None
        self.player2 = None

        #obstacles
        self.walls = []

        #création des joueurs et des obstacles
        self.create_players()
        self.create_obstacles()

    #création des deux joueurs
    def create_players(self) : 
        image_players = pygame.image.load("assets/cowboy.png")

        image1 = image_players.copy()
        image1 = pygame.transform.scale(image_players, (96, 96))
        image1.set_colorkey((255, 255, 255))
        self.player1 = PlayerShooter(self.screen, image1, (80, 360))

        image2 = image1.copy()
        image2 = pygame.transform.flip(image2, True, False)
        image2.set_colorkey((255, 255, 255))
        self.player2 = PlayerShooter(self.screen, image2, (1000, 360))

    #création des deux obstacles
    def create_obstacles(self) : 
        pass

    def set(self) : 
        self.etat = True

        sound.background_music.stop()
        sound.countdown_sound.play()

    def unset(self) :
        self.etat = False

        sound.game_music.stop()
        sound.countdown_sound.stop()
        sound.victory_sound.stop()
        sound.draw_sound.stop()
        sound.defeat_sound.stop()
        sound.background_music.play(loops=-1)

    #affiche les éléments de la partie
    def draw(self) :

        #affiche le fond d'écran
        self.screen.blit(self.background, (0,0))

        #affichage de la partie tant que celle-ci n'est pas finie
        if not(self.game_over_etat) : 
            
            #affiche les deux joueurs
            self.player1.draw()
            self.player2.draw()

            #affichage des projectiles
            for bullet in self.player1.projectiles :
                bullet.draw()
            for bullet in self.player2.projectiles :
                bullet.draw()

        else : 
            pass

    #applique les actions de la partie
    def apply(self) :

        #actions de la partie tant que celle-ci n'est pas finie
        if not(self.game_over_etat) : 
            #applique les actions des joueurs
            self.player1.apply()
            self.player2.apply()

            #mouvement des projectiles
            for bullet in self.player1.projectiles : 
                bullet.apply()
                if bullet.rect.colliderect(self.player2.rect) : 
                    self.player1.projectiles.remove(bullet)
                    self.player2.life -= 1
                if bullet.rect.left <= 0 or bullet.rect.right >= 1080 :
                    self.player1.projectiles.remove(bullet)

            for bullet in self.player2.projectiles :
                bullet.apply()
                if bullet.rect.colliderect(self.player1.rect) : 
                    self.player2.projectiles.remove(bullet)
                    self.player1.life -= 1
                if bullet.rect.left <= 0 or bullet.rect.right >= 1080:
                    self.player2.projectiles.remove(bullet)

            #fin de la partie
            if self.player1.life <= 0 : 
                self.game_over(2)
            elif self.player2.life <= 0 : 
                self.game_over(1)

        else : 
            if self.end_countdown() == True : 
                self.unset()

    #contrôle les évènements en lien avec la partie
    def manage_events(self, event) : 
        if event.type == pygame.KEYDOWN : 
            #bouton du joueur 1
            if event.key == pygame.K_a : 
                self.player1.attack()
            #bouton du joueur 2
            elif event.key == pygame.K_p : 
                self.player2.attack()

    def game_over(self, joueur) : 
        self.game_over_etat = True
        self.time_start_game_over = pygame.time.get_ticks()

    def start_countdown(self) : 
        pass

    def end_countdown(self) : 
        return pygame.time.get_ticks() - self.time_start_game_over >= self.end_countdown_delay 

class GameSolo(Game) : 
    def __init__(self, screen, police1, police2, police3, police4):
        super().__init__(screen, police1, police2, police3, police4)