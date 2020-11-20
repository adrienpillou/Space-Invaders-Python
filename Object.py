import pygame

# Object class
class Object():
    def __init__(self, name, tag):
        self.name = name
        self.tag = tag
        self.position = (0, 0)
        self.image = None
        self.width = 0
        self.height = 0
        self.velocity = (0, 0)

    def __repr__(self):
        return f"Object {self.name} at position {self.position}"

    def set_tag(self, tag:str):
        self.tag = tag
    
    def set_position(self, position):
        self.position = position

    def set_velocity(self, velocity):
        self.velocity = velocity
    
    def get_x(self):
        return self.position[0]
    
    def get_y(self):
        return self.position[1]

    def get_rect(self):
        return (self.get_x(), self.get_y(), self.width, self.height)
        
    def draw(self, surface):
        if self.image == None:
            return
        surface.blit(self.image, self.position)
    
    def tint(self, color):
        mask = pygame.surface.Surface(self.image.get_size())
        mask.fill(color)
        self.image.blit(mask, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)

    def load_image(self, image_path):
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (self.width, self.height))
        return image
    
    def set_image(self, image):
        image.set_colorkey((0, 0, 0))
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()

    def upscale(self, multiplier):
        self.image = pygame.transform.scale(self.image, (self.width*multiplier, self.height*multiplier))
