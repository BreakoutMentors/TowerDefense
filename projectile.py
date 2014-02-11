import pygame, math

class Projectile(pygame.sprite.Sprite):
    image = None

    def __init__(self,tower,target):
        pygame.sprite.Sprite.__init__(self)
        
        if Projectile.image is None:
                # This is the first time this class has been
                # instantiated. So, load the image for this and
                # all subsequence tower instances.
                Projectile.image = pygame.image.load("arrow.png")
        self.image = Projectile.image

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.x = tower.x
        self.y = tower.y
        self.speed = 4 #projectile goes 4 times the game speed
        self.rect.center = (self.x, self.y)
        #determine the angle between the tower and balloon, rotate image
        dx = target.x - tower.x
        dy = target.y - tower.y
        self.rads = math.atan2(dy,dx)
        self.image = pygame.transform.rotate(self.image, -math.degrees(self.rads)-90)

    def move(self,game_speed):
       self.x = self.x + math.cos(self.rads) * game_speed * self.speed
       self.y = self.y + math.sin(self.rads) * game_speed * self.speed
       self.rect.center = (self.x, self.y)
