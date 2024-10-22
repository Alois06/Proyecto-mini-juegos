import pygame
import sys

from game import Game
from menu import Menu_Principal, Menu_2players, Menu_Solo
from sound import sound

#initialisation du module pygame
pygame.init()
pygame.font.init()

#création de la fenêtre de jeu
dimensions = (1080, 720)
pygame.display.set_caption("Multi Game")
screen = pygame.display.set_mode(dimensions)

#création de l'objet qui va permettre de gérer le temps
time = pygame.time.Clock()

#création des polices
police1 = pygame.font.Font("assets/polices/good timing bd.ttf", 30)
police2 = pygame.font.Font("assets/polices/good timing bd.ttf", 27)
police3 = pygame.font.Font("assets/polices/DigitalDream.ttf", 30)
police4 = pygame.font.Font("assets/polices/Pixel Digivolve.otf", 35)
police3.bold = True

#image de fond d'écran
background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, dimensions)

#son
sound.change_volume()
sound.background_music.play(loops=-1)

#création des classes des différents menus
menu = Menu_Principal(screen, police1, police2)
menu_solo = Menu_Solo(screen, police1, police2)
menu_2players = Menu_2players(screen, police1, police2)

#création de la classe du jeu
game = Game(screen, police1, police2, police3, police4)

#DEBUT DE LA BOUCLE DE JEU

game_on = True

while game_on : 

    #efface l'arrière plan
    screen.fill(0)

    #boucle qui gère les évènements (mouvements et clics de souris, appuis de bouton, etc)
    for event in pygame.event.get() :

        #quitte la fenêtre
        if event.type == pygame.QUIT : 
            game_on = False

        #vérifie si un bouton est appuyé
        if event.type == pygame.MOUSEBUTTONDOWN :

            if menu.etat : 
                if menu.button_play_solo.click() :
                    menu.unset()
                    menu_solo.set()
                elif menu.button_play_2_players.click():
                    menu.unset()
                    menu_2players.set()
            
            elif menu_solo.etat : 
                if menu_solo.button_game1.click() :
                    menu_solo.unset()
                    game = Game(screen, police1, police2, police3, police4)
                    game.set()
                elif menu_solo.button_return.click() :
                    menu_solo.unset()
                    menu.set()

            elif menu_2players.etat : 
                if menu_2players.button_game1.click() :
                    menu_2players.unset()
                    game = Game(screen, police1, police2, police3, police4)
                    game.set()
                elif menu_2players.button_return.click() :
                    menu_2players.unset()
                    menu.set()

        elif game.etat : 
            game.manage_events(event)

    #affichage de l'image d'arrière plan
    screen.blit(background, (0, 0))

    #affichage des éléments du menu/jeu en cours
    if menu.etat :
        menu.draw()

    elif menu_solo.etat :
        menu_solo.draw()

    elif menu_2players.etat : 
        menu_2players.draw()

    elif game.etat :
        game.apply() 
        game.draw()
        if game.etat == False :
            menu.set()

    #actualisation de l'écran
    pygame.display.flip()
    time.tick(30) #fait trourner le jeu à 30 fps

#quitte la fenêtre de jeu pygame et met fin au programme
pygame.quit()
sys.exit()