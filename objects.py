import pygame
import random
import math
import tools
from sound import sound

#Objets pour le jeu de raquette

class Ball :
    def __init__(self, screen, image: pygame.Surface, coords) : 
        self.screen = screen

        #création de la balle
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = coords

        #vecteur déplacement
        lx = [-x for x in range(2, 6)] + [x for x in range (2, 6)]
        ly = [-y for y in range(2, 6)] + [y for y in range (2, 6)]
        self.vx = lx[random.randint(0, 7)]
        self.vy = ly[random.randint(0, 7)]

        #vitesse et accélération
        self.v = math.sqrt(self.vx**2 + self.vy**2)
        self.a = 1

    #Bouge la balle en x et en y
    def move(self) : 
        self.rect.x += self.vx*self.a
        self.rect.y += self.vy*self.a
        self.v = math.sqrt((self.vx*self.a)**2 + (self.vy*self.a)**2)

    def apply(self, walls: list, rackets: list) :

        if self.rect.top <= 0 or self.rect.bottom >= 720 or self.rect.left <= 0 or self.rect.right >= 1080 :
            sound.ball_sound.play()

            if self.rect.top <= 0 :
                self.vy = abs(self.vy)
                
            elif self.rect.bottom >= 720: 
                self.vy = -abs(self.vy)

            if self.rect.left <= 0 :
                self.vx = abs(self.vx)
            
            elif self.rect.right >= 1080 :
                self.vx = -abs(self.vx)

        for obstacle in walls + rackets : 

            obstacle_obj = obstacle
            obstacle = obstacle.rect

            original_vx = self.vx
            original_vy = self.vy

            if self.rect.colliderect(obstacle) :

                sound.ball_sound.play()

                #Touche le haut ou le bas d'un obstacle
                if (self.rect.left > obstacle.left and self.rect.right < obstacle.right):
                    if self.rect.top > obstacle.top and self.rect.top < obstacle.bottom :
                        self.vy = abs(self.vy)
                    elif self.rect.bottom > obstacle.top and self.rect.bottom < obstacle.bottom : 
                        self.vy = -abs(self.vy)
                
                #Touche le côté gauche ou droite d'un obstacle
                if self.rect.top > obstacle.top and self.rect.bottom < obstacle.bottom : 
                    if self.rect.left > obstacle.left and self.rect.left < obstacle.right :
                        self.vx = abs(self.vx)
                    elif self.rect.right > obstacle.left and self.rect.right < obstacle.right : 
                        self.vx = -abs(self.vx)

                #Touche un angle
                if original_vx == self.vx and original_vy == self.vy :

                    if self.rect.collidepoint(obstacle.bottomright) : 
                        dx = obstacle.right - self.rect.left
                        dy = obstacle.bottom - self.rect.top

                        if self.vx < 0 and self.vy < 0 and abs(dx-dy) <= 2 :
                            self.vx = abs(self.vx)
                            self.vy = abs(self.vy)
                        elif self.vx < 0 and self.vy > 0 : 
                            self.vx = abs(self.vx)
                        elif self.vx > 0 and self.vy < 0 : 
                            self.vy = abs(self.vy)
                        else : 
                            comparaison = tools.compare_impact(dx, dy, self.vx, self.vy)
                            self.vx, self.vy = comparaison[0], comparaison[1]
                    
                    if self.rect.collidepoint(obstacle.topright) : 
                        dx = obstacle.right - self.rect.left
                        dy = abs(obstacle.top - self.rect.bottom)
                        
                        if self.vx < 0 and self.vy > 0 and abs(dx-dy) <= 2 :
                            self.vx = abs(self.vx)
                            self.vy = -abs(self.vy)
                        elif self.vx < 0 and self.vy < 0 : 
                            self.vx = abs(self.vx)
                        elif self.vx > 0 and self.vy > 0 : 
                            self.vy = -abs(self.vy)
                        else : 
                            comparaison = tools.compare_impact(dx, dy, self.vx, self.vy)
                            self.vx, self.vy = comparaison[0], comparaison[1]

                    if self.rect.collidepoint(obstacle.topleft) : 
                        dx = abs(obstacle.left - self.rect.right)
                        dy = abs(obstacle.top - self.rect.bottom)

                        if self.vx > 0 and self.vy > 0 and abs(dx-dy) <= 2 :
                            self.vx = -abs(self.vx)
                            self.vy = -abs(self.vy)
                        elif self.vx > 0 and self.vy < 0 : 
                            self.vx = -abs(self.vx)
                        elif self.vx < 0 and self.vy > 0 : 
                            self.vy = -abs(self.vy)
                        else : 
                            comparaison = tools.compare_impact(dx, dy, self.vx, self.vy)
                            self.vx, self.vy = comparaison[0], comparaison[1]

                    if self.rect.collidepoint(obstacle.bottomleft) : 
                        dx = abs(obstacle.left - self.rect.right)
                        dy = obstacle.bottom - self.rect.top
                        
                        if self.vx > 0 and self.vy < 0 and abs(dx-dy) <= 2 :
                            self.vx = -abs(self.vx)
                            self.vy = abs(self.vy)
                        elif self.vx > 0 and self.vy > 0 : 
                            self.vx = -abs(self.vx)
                        elif self.vx < 0 and self.vy < 0 : 
                            self.vy = abs(self.vy)
                        else : 
                            comparaison = tools.compare_impact(dx, dy, self.vx, self.vy)
                            self.vx, self.svy = comparaison[0], comparaison[1]
                
                #obstacles avec rebond aléatoire ou téléportation
                if type(obstacle_obj) == ObstacleRebond or type(obstacle_obj) == ObstacleTeleportation :
                    obstacle_obj.effect(self)

        #Applique le mouvement de la balle
        self.move()

    #Affiche la balle sur la fenêtre de jeu
    def draw(self) : 
        self.screen.blit(self.image, self.rect)

class SpriteY(pygame.sprite.Sprite) :
    def __init__(self, screen, image: pygame.Surface, coords) :
        super().__init__()

        self.screen = screen

        #création du sprite
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = coords

        #vecteur déplacement
        self.vy = -5

    def draw(self) : 
        self.screen.blit(self.image, self.rect)

    def move(self) :
        self.rect.y += self.vy
    
    def apply(self) : 
        if self.rect.bottom >= 720 :
            self.vy = -abs(self.vy)
        elif self.rect.top <= 0 :
            self.vy = abs(self.vy)

        self.move()    

class Racket(SpriteY) : 
    def __init__(self, screen, image: pygame.Surface, coords):
        super().__init__(screen, image, coords)

        #accélération
        self.a = 1

    def move(self) :
        self.rect.y += self.vy*self.a

class Obstacle(pygame.sprite.Sprite) :
    def __init__(self, screen, image:pygame.surface.Surface, coords) :

        super().__init__()

        self.screen = screen

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = coords
        
    def draw(self) : 
        self.screen.blit(self.image, self.rect)

    def move(self, coords) : 
        self.rect.center = coords

class ObstacleRebond(Obstacle) :
    def __init__(self, screen, image, coords):
        super().__init__(screen, image, coords)

    def effect(self, ball:Ball) :
        x_sign = ball.vx/abs(ball.vx)
        y_sign = ball.vy/abs(ball.vy)

        ball.vx = random.randint(2, 5)*x_sign
        ball.vy = random.randint(2, 5)*y_sign

class ObstacleTeleportation(Obstacle) :
    def __init__(self, screen, image, coords, coords_tp):
        super().__init__(screen, image, coords)

        self.coords_tp = coords_tp

    def effect(self, ball:Ball) :
        ball.rect.center = self.coords_tp
        ball.vx = random.randint(2, 5)*[-1, 1][random.randint(0, 1)]
        ball.vy = random.randint(2, 5)*[-1, 1][random.randint(0, 1)]

class ObstacleMouvant(Obstacle) :
    def __init__(self, screen, image, coords, cos, sin, v, d_trajectoire):
        super().__init__(screen, image, coords)

        #coordonnées du mouvement
        self.vx = cos*v
        self.vy = sin*v

        if cos != 0 :
            self.sign_cos = cos/abs(cos)
        if sin != 0 :
            self.sign_sin = sin/abs(sin)
        
        #coordonnées des deux bouts de la trajectoire
        self.coords_max = (int(cos*(d_trajectoire/2) + coords[0]), int(sin*(d_trajectoire/2) + coords[1]))
        self.coords_min = (int(-cos*(d_trajectoire/2) + coords[0]), int(-sin*(d_trajectoire/2) + coords[1]))
        
        xs = [self.coords_max[0], self.coords_min[0]]
        ys = [self.coords_max[1], self.coords_min[1]]
        self.xmax, self.xmin = max(xs), min(xs)
        self.ymax, self.ymin = max(ys), min(ys)

        #rect trajectoire
        dx = self.xmax - self.xmin
        dy = self.ymax - self.ymin
        self.rect_trajectoire = pygame.rect.Rect(self.xmin, self.ymin, dx, dy)

        #accélération
        self.a = 1

    def move(self) :
        self.rect.x += self.vx*self.a
        self.rect.y += self.vy*self.a

    def apply(self) :
        if not(self.rect_trajectoire.collidepoint(self.rect.center)) :
            if ((self.rect.center[0] < self.xmin and self.sign_cos < 0) or (self.rect.center[0] > self.xmax and self.sign_cos > 0)) or (self.rect.center[1] < self.ymin and self.sign_sin < 0) or (self.rect.center[1] > self.ymax and self.sign_sin > 0) :
                self.vx = -self.sign_cos*abs(self.vx)
                self.vy = -self.sign_sin*abs(self.vy)
            elif (self.rect.center[0] < self.xmin and self.sign_cos > 0) or (self.rect.center[0] > self.xmax and self.sign_cos < 0) or (self.rect.center[1] < self.ymin and self.sign_sin > 0) or (self.rect.center[1] > self.ymax and self.sign_sin < 0) :
                self.vx = self.sign_cos*abs(self.vx)
                self.vy = self.sign_sin*abs(self.vy)

        self.move()
            