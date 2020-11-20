import pygame
import os
from Object import Object

class Shelter(Object):
    def __init__(self, name, tag):
        super().__init__(name, tag)
        self.max_hp = 5
        self.hp = self.max_hp
        
        