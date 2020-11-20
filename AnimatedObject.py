from Object import Object

class AnimatedObject(Object):
    def __init__(self, name, tag):
        super().__init__(name, tag)
        self.images = []
        self.frame_index = 0
        self.animation_speed = 1
        self.loop = True
        self.animation_timer = 1

    def set_animation_speed(self, animation_speed):
        self.animation_speed = animation_speed

    def set_images(self, images):
        for image in images:
            image.set_colorkey((0, 0, 0))
            self.images.append(image)
    
    def add_image(self, image):
        image.set_colorkey((0, 0, 0))
        self.images.append(image)

    def draw(self, surface):
        surface.blit(self.images[self.frame_index], self.position)

    def animate(self, dt):
        if(len(self.images) <= 1):
            return
        self.animation_timer -= self.animation_speed * dt
        if self.animation_timer <= 0:
            self.animation_timer = 1
            if(self.frame_index == len(self.images)-1):
                self.frame_index = 0
            else:
                self.frame_index += 1
    
    def next_frame(self):
        if(self.frame_index < len(self.images)-1):
            self.frame_index += 1
        else : 
            self.frame_index = 0 

    def previous_frame(self):
        if(self.frame_index > 0):
            self.frame_index -= 1
        else:
            self.frame_index = len(self.images)-1 