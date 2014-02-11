import pygame

class Balloon(pygame.sprite.Sprite):
    image = None
    direction_turn_points = [("right",665),("down",515),("left",115),("up",-100)]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        if Balloon.image is None:
                # This is the first time this class has been
                # instantiated. So, load the image for this and
                # all subsequence balloon instances.
                Balloon.image = pygame.image.load("7.png")
        self.image = Balloon.image

        self.rect = self.image.get_rect()
        self.direction = 0 #starts moving off in the first direction
        self.x = -20
        self.y = 85
        self.rect.center = (self.x, self.y) 

    def move(self, speed):
        #get the string for the current direction the balloon is traveling
        current_direction = Balloon.direction_turn_points[self.direction][0]
        turn_pixel = Balloon.direction_turn_points[self.direction][1]
        if current_direction == "left":
            self.x = self.x - speed
            if self.x < turn_pixel:
                self.direction = self.direction + 1
        elif current_direction == "right":
            self.x = self.x + speed
            if self.x > turn_pixel:
                self.direction = self.direction + 1
        elif current_direction == "up":
            self.y = self.y - speed
            if self.y < turn_pixel:
                self.direction = self.direction + 1
        elif current_direction == "down":
            self.y = self.y + speed
            if self.y > turn_pixel:
                self.direction = self.direction + 1
        self.rect.center = (self.x, self.y) 
