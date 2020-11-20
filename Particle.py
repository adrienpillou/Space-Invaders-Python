import pygame
import time
from Object import Object

# Static particle image
class Particle(Object):
    def __init__(self, name, tag, lifetime):
        super().__init__(name, tag)
        self.lifetime = lifetime
        self.start_time = time.time()

    def update(self, dt):
        self.lifetime -= dt