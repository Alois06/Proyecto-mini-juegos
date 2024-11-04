import pygame

import random
import math

from sound import sound
import tools

#classe de la partie normale
class Game :
    def __init__(self, screen, police1, police2, police3, police4) :
        self.screen = screen

        self.etat = False

        self.police1 = police1
        self.police2 = police2
        self.police3 = police3
        self.police4 = police4

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

    def draw(self) :
        pass

    def apply(self) :
        pass

    def manage_events(self) : 
        pass
