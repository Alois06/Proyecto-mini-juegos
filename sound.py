import pygame

class Sound : 
    def __init__(self) : 
        self.sound_on = False

        self.background_music = pygame.mixer.Sound("assets/sounds/background.mp3")

        self.select_sound = pygame.mixer.Sound("assets/sounds/select_sound.mp3")

        self.game_music = pygame.mixer.Sound("assets/sounds/game_music.mp3")

        self.ball_sound = pygame.mixer.Sound("assets/sounds/ball_impact.mp3")

        self.countdown_sound = pygame.mixer.Sound("assets/sounds/countdown.mp3")

        self.alert_sound = pygame.mixer.Sound("assets/sounds/alert.mp3")

    def stop(self) :
        pygame.mixer.stop()

    def volume_on(self) : 
        self.background_music.set_volume(1.0)
        self.select_sound.set_volume(0.3)
        self.game_music.set_volume(1.0)
        self.ball_sound.set_volume(1.0)
        self.countdown_sound.set_volume(1.0)
        self.alert_sound.set_volume(0.75)

    def volume_off(self) : 
        self.background_music.set_volume(0)
        self.select_sound.set_volume(0)
        self.game_music.set_volume(0)
        self.ball_sound.set_volume(0)
        self.countdown_sound.set_volume(0)
        self.alert_sound.set_volume(0)

    def change_volume(self) :
        self.sound_on = not(self.sound_on)

        if self.sound_on : 
            self.volume_on()
        else : 
            self.volume_off()

pygame.mixer.init()

sound = Sound()