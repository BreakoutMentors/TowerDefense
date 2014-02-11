import pygame, math

class Tower(pygame.sprite.Sprite):
    image = None
    max_reload_time = 50

    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        
        if Tower.image is None:
                # This is the first time this class has been
                # instantiated. So, load the image for this and
                # all subsequence tower instances.
                Tower.image = pygame.image.load("ghost.png")
        self.image = Tower.image

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.center = (self.x, self.y)
        self.reload_time = 0 #time left to wait between shots
        self.reload_max = 150 #how long it should take between shots
        self.range = 200 #max pixels to balloon in order to shoot at it


    def shoot(self):
        self.reload_time = self.reload_max
   
    def canShoot(self):
        if self.reload_time <= 0:
            return True
        else:
            return False

    def decreaseReload(self,game_speed):
        self.reload_time = self.reload_time - game_speed

    def getCloseBalloon(self,balloon_list):
        for balloon in balloon_list:
            if self.distance(balloon) <= self.range:
                return balloon
        return None

    def distance(self,balloon):
        dist = (self.x-balloon.x)*(self.x-balloon.x) + (self.y-balloon.y)*(self.y-balloon.y)
        dist = math.sqrt(dist)
        return dist
