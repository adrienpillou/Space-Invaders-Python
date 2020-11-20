from Object import Object

class Ship(Object):
    def __init__(self, name):
        super().__init__(name, "ENEMY")
        self.direction = 1
