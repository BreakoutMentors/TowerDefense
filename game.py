import pygame
from balloon import *
from tower import *
from projectile import *
pygame.init()
screen = pygame.display.set_mode([800,600])
white = [255, 255, 255]

#the game's functions
def isValidTowerSpot(x,y):
    for track_rect in track_rectangles:
        #make a pygame rect 37 pixels bigger left right up and down (half the tower width)
        pygame_rect = pygame.Rect(track_rect[0]-37,track_rect[1]-37,track_rect[2]+72,track_rect[3]+72,)
        if pygame_rect.collidepoint(x,y):
            return False
    return True

def createTowerIfAllowed(x,y):
    global money
    if money >= 200 and isValidTowerSpot(x,y):
        new_tower = Tower(x,y)
        tower_list.append(new_tower)
        money = money - 200

def draw_everything():
    #make the screen completely white
    screen.fill(white)
    #draw the track
    for rect in track_rectangles:
        pygame.draw.rect(screen, track_color, rect)
    #draw everything else
    score_label = myfont.render("$"+str(money), 1, pygame.color.THECOLORS['black'])
    screen.blit(score_label, (700, 30))
    health_label = myfont.render("Health: "+str(health), 1,pygame.color.THECOLORS['black'])
    screen.blit(health_label, (700, 10))
    for bloon in balloon_list:
        screen.blit(bloon.image, bloon.rect)
    for tower in tower_list:
        screen.blit(tower.image, tower.rect)
    for bullet in bullet_list:
        screen.blit(bullet.image, bullet.rect)
    #update the entire display
    pygame.display.update()

#the game's variables
track_color = (120,120,120)
myfont = pygame.font.SysFont("Arial", 22)
money = 200
game_speed = 3
balloon_list = []
balloons_created = 0
ballon_gameloop_counter = 0
health = 100
tower_list = []
track_rectangles = [[0, 60, 690, 50], [640, 60, 50, 480], [85, 490, 560, 50], [85, 0, 50, 500]]
bullet_list = []
waves = [(40,20),(20,30),(15,30),(6,40),(6,40)] #(creation rate, ballons in wave)
current_wave = 0

running = True
#game loop
while running:
    for event in pygame.event.get():
        #check if you've exited the game
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            createTowerIfAllowed(mouse_x, mouse_y)
            
    #pause for 20 milliseconds
    pygame.time.delay(20)

    balloon_creation_rate = waves[current_wave][0]
    max_balloons = waves[current_wave][1]
    #determine whether to create a new balloon
    if ballon_gameloop_counter == balloon_creation_rate and balloons_created < max_balloons:
        ballon_gameloop_counter = 0
        new_balloon = Balloon()
        balloon_list.append(new_balloon)
        balloons_created = balloons_created + 1
        #if we have created all the balloons for this wave and there is another wave
        if balloons_created == max_balloons and current_wave < len(waves)-1:
            current_wave = current_wave + 1
            ballon_gameloop_counter = -700 #the pause between waves
            balloons_created = 0
    ballon_gameloop_counter = ballon_gameloop_counter + 1

    #move all the balloons and see if they left the screen
    for bloon in balloon_list:
        bloon.move(game_speed)
        if bloon.y < 0:
            balloon_list.remove(bloon)
            health = health - 1

    #change the tower reload time and see if any balloons can be shot at
    for tower in tower_list:
        tower.decreaseReload(game_speed)
        if tower.canShoot():
            #determine if a balloon is within range
            target = tower.getCloseBalloon(balloon_list)
            if target != None:
                new_bullet = Projectile(tower,target)
                bullet_list.append(new_bullet)
                tower.shoot()

    #move all the bullets and see if they hit a balloon
    for bullet in bullet_list:
        bullet.move(game_speed)
        #collidelist funtion returns the index in the list that was hit or -1 if nothing hit
        colliding_balloon_index = bullet.rect.collidelist(balloon_list)
        if  colliding_balloon_index != -1:
            colliding_balloon = balloon_list[colliding_balloon_index]
            balloon_list.remove(colliding_balloon)
            bullet_list.remove(bullet)
            money = money + 10

    #call our function to draw everything on the screen
    draw_everything()

pygame.quit()
