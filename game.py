import pygame
import random
import sys

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

# Define the Player object extending pygame.sprite.Sprite
# The surface we draw on the screen is now a property of 'player'
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image_still = pygame.image.load("rabbit_forward_still.png").convert_alpha()
        self.image_run1 = pygame.image.load("rabbit_forward_half.png").convert_alpha()
        self.image_run2 = pygame.image.load("rabbit_forward_jump.png").convert_alpha()
        self.surf = self.image_still
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf,(SCALE,SCALE))
        self.rect = self.surf.get_rect(center=(128,240))
        self.cooldown=0
        self.angle=0

    # Move the sprite based on keypresses
    def update(self, pressed_keys):
        if(self.cooldown <= 0):
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -16)
                self.cooldown = 5
                self.angle=0
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 16)
                self.cooldown = 5
                self.angle=180
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-16, 0)
                self.cooldown = 5
                self.angle=90
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(16, 0)
                self.cooldown = 5
                self.angle=270
        elif(self.cooldown >=1):
            self.cooldown = self.cooldown -1
        if(self.cooldown >=3):
            self.surf = self.image_run2
        else:
            self.surf = self.image_still
        self.surf = pygame.transform.rotate(self.surf,self.angle)
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
        self.surf = pygame.image.load("blue_van.png").convert_alpha()
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
        self.surf = pygame.image.load("castledoors.png").convert_alpha()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.surf = pygame.transform.scale(self.surf,(SCALE,SCALE)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, 15)*SCALE,
                8,
            )
        )



class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        
# Initialize pygame
pygame.init()
clock = pygame.time.Clock()
BackGround = Background('map0.png', [0,0])
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy.
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 2000)

# Create our 'player'
player = Player()

# Create groups to hold enemy sprites, and every sprite
# - enemies is used for collision detection and position updates
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
doors = pygame.sprite.Group()
# Variable to keep our main loop running
running = True
cooldown = 0

new_door=Door()
doors.add(new_door)
all_sprites.add(new_door)

# Our main loop
while running:

    # Look at every event in the queue
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
    if pygame.sprite.spritecollide(player, doors, dokill=False):
       player.kill()
       running = False

    clock.tick(60)
    # Flip everything to the display
    pygame.display.flip()
pygame.quit()

