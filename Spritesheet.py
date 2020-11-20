from xml.dom import minidom
import pygame

class spritesheet():
    def __init__(self, image_path):
        self.image_path = image_path
        self.descriptive_file_path = ""
        self.sprite_tag_name = "sprite"
        self.image = self.load_image()
        self.sprites = dict()
        self.items = None

    def add_descriptive(self, descriptive_file_path, sprite_tag_name = "sprite"):
        self.descriptive_file_path = descriptive_file_path
        self.sprite_tag_name = sprite_tag_name
        self.xml_descriptive = self.read_descriptive()
        self.items = self.get_items()

    def read_descriptive(self):
        xml_doc = minidom.parse(self.descriptive_file_path)
        return xml_doc

    def get_items(self):
        items = self.xml_descriptive.getElementsByTagName(self.sprite_tag_name)
        return items

    def get_item_attributes(self, index):
        attribute_dict = dict(self.items[index].attributes.items())
        return attribute_dict
        
    def load_image(self):
        image = pygame.image.load(self.image_path)
        return image
    
    def slice_sprites(self):
        for index in range(len(self.items)):
            # Gathering attributes
            sprite_attributes = self.get_item_attributes(index)
            sprite_id = sprite_attributes['id']
            sprite_width = int(sprite_attributes['w'])
            sprite_height = int(sprite_attributes['h'])
            sprite_position = (int(sprite_attributes['x']), int(sprite_attributes['y']))
            
            # Creating and blitting the image into the sprite
            sprite_image = pygame.Surface((sprite_width, sprite_height))
            sprite_image.blit(self.image, (0, 0), (sprite_position[0], sprite_position[1], sprite_width, sprite_height))
            
            # Add the sprite with a given id to a dictionnary
            self.sprites[sprite_id] = sprite_image
    
    def get_sprite(self, key:str):
        if key in self.sprites:
            return self.sprites[key]
        else:
            print(f"Sprite key '{key}' does not exists !")
            

    def set_color_to_alpha(self, color = (0, 0, 0)):
        self.image.set_colorkey(color)

            




