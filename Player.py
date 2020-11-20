import pygame
from Object import Object
from Alarm import alarm

class player(Object):

    def __init__(self, name, tag):
        super().__init__(name, tag)
        self.speed = 200
        self.can_shoot = True
        self.can_move = True
        self.rate_of_fire = 300/1000
        self.shooting_alarm = alarm(self.rate_of_fire)
        self.is_shooting = False

    def move(self, x_dir, y_dir, speed):
        x = self.get_x()
        y = self.get_y()
        x = x + (x_dir*speed)
        y = y + (y_dir*speed)
        self.set_position((x, y))

    def get_can_shoot(self):
        if self.shooting_alarm.is_ended():
            self.can_shoot = True

        return self.can_shoot

    '''def load_assets(self):
        self.sprite = pygame.image.load(os.path.join('assets', 'player.bmp'))
        self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))'''