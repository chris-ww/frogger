import pygame
import random
import sys
import pictures

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)



SCALE = 16
SCREEN_SIZE=SCALE*16
SCREEN_WIDTH = SCREEN_SIZE
SCREEN_HEIGHT = SCREEN_SIZE
MAP=0

class Game(map=0,scale=16):
    def __init__(self):
        self.map=map
        self.scale=scale
        self.screen = pygame.display.set_mode((scale*16, scale*16))
        self.player = Player()
        self.enemies=pygame.sprite.Group()
        self.all_sprites=pygame.sprite.Group()
        self.all_sprites.add(PLAYER)
        self.doors=pygame.sprite.Group()
        self.running=True
        new_door=Door()
        self.doors.add(new_door)
        self.all_sprites.add(new_door)
        ADDENEMY = pygame.USEREVENT + 1
        pygame.time.set_timer(ADDENEMY, 2000)
        
    def Update:
        for event in pygame.event.get():
            # Did the user hit a key?
        if event.type == KEYDOWN:
                # Was it the Escape key? If so, stop the loop
            if event.key == K_ESCAPE:
                running = False
    
            # Did the user click the window close button? If so, stop the loop
        elif event.type == QUIT:
            running = False
    
            # Should we add a new enemy?
        elif event.type == ADDENEMY:
                # Create the new enemy, and add it to our sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
    
        # Get the set of keys pressed and check for user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
    
            
        # Update the position of our enemies
        if(MAP !=0):
            enemies.update()
    
        # Fill the screen with black
        screen.fill([255, 255, 255])
        screen.blit(BackGround.image, BackGround.rect)
    
        # Draw all our sprites
        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
    
        # Check if any enemies have collided with the player
        if pygame.sprite.spritecollideany(player, enemies):
            # If so, remove the player and stop the loop
           player.kill()
           running = False
           end='end'
        if pygame.sprite.spritecollide(player, doors, dokill=False):
           player.kill()
           running = False
           end='win'
        if(player !='cpu-learn'):
            clock.tick(60)
        # Flip everything to the display
        pygame.display.flip()
        print(pygame.PixelArray(screen))
    pygame.quit()
    print(end)        


    end='dnf'
        pygame.init()
        
# Define the Player object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("pictures/frog.png").convert_alpha()
        self.surf = self.image
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf,(SCALE,SCALE))
        if(MAP == 0):
            self.rect = self.surf.get_rect(center=(random.randint(0, 15)*SCALE+int(SCALE/2),random.randint(0, 15)*SCALE+int(SCALE/2)))
        else:
            self.rect = self.surf.get_rect(center=(int(SCREEN_SIZE/2),int(SCALE*15.5)))
        self.cooldown=0
        self.angle=0
        

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if(self.cooldown <= 0):
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -16)
                self.cooldown = 5
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 16)
                self.cooldown = 5
                self.angle=180
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-16, 0)
                self.cooldown = 5
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(16, 0)
                self.cooldown = 5
        elif(self.cooldown >=1):
            self.cooldown = self.cooldown -1

        self.surf = pygame.transform.scale(self.surf,(SCALE,SCALE))


        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


# Define the enemy object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'enemy'
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("pictures/blue_van.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf,(SCALE*2,SCALE))
        # The starting position is randomly generated, as is the speed
        self.rect = self.surf.get_rect(
            center=(
                -20,
                208,
            )
        )
        self.speed = 5

    # Move the sprite based on speed
    # Remove it when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.left > 256:
            self.kill()

# Define the enemy object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'enemy'
class Door(pygame.sprite.Sprite):
    def __init__(self):
        super(Door, self).__init__()
        self.surf = pygame.image.load("pictures/castledoors.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf,(SCALE,SCALE))
        if(MAP == 0):
            self.rect = self.surf.get_rect(
                center=(
                    random.randint(0, 15)*SCALE+ int(SCALE/2),
                    random.randint(0, 15)*SCALE+ int(SCALE/2),
                    )
                )



class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


def Play(scale = 16, MAP = 0, player = 'human'):
    
    clock = pygame.time.Clock()
    
    
    # Our main loop
    while running:
        Update(screen,player,all_sprites,doors,player)
        


    