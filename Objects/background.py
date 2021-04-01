class Background:
    def __init__(self, x, y, w, h, image):
        self.x, self.y, self.w, self.h, self.image = x, y, w, h, image
        self.collide = False
        self.collectable = False

    def draw(self, display,camera):
        display.blit(self.image, (self.x+camera.x, self.y+camera.y))

    def update(self, keys):
        pass
