import pygame
import os
from Alarm import alarm
from AnimatedObject import AnimatedObject

class alien(AnimatedObject):
    def __init__(self, name, tag, type):
        super().__init__(name, tag)
        self.type = type
        self.width = 16
        self.height = 8
    
    def get_type(self):
        return self.type