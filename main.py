import pygame
import random
import math
from pygame import mixer


# Initialise the pygame
pygame.init()

# To create a new screen
screen = pygame.display.set_mode((800, 600))

# Create a variable to keep the program running
running = True

# Background
background = pygame.image.load('background.jpg')

# Title and icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo-flying.png')
pygame.display.set_icon(icon)

#BGM
mixer.music.load('background.wav')
mixer.music.play(-1)

#Game over
def game_over() :
    gameoverImg = pygame.image.load('game over.png')
    screen.blit(gameoverImg, (0, 0))
    score = font.render('YOU SCORED : ' + str(score_value), True, (255, 255, 255))
    screen.blit(score, (350, 480))
    pygame.display.update()

# Player
playerImg = pygame.image.load('arcade-game.png')
playerX = 400  # X-coordinate
playerY = 450  # Y-coordinate

def player(x, y):  # Define a function for player
    screen.blit(playerImg, (x, y))  # Blit means 'draw'


# Bullet
# ready - can't see bulet
# fire - bullet is shot
bulletImg = pygame.image.load('bullet (1).png')
bulletX = 0
bulletY = 450
bulletX_change = 0
bulletY_change = 4
bullet_state = 'ready'

def bullet_fire(x, y):  # Define a function for bullet
    global bullet_state  # global to access the bullet_state variable inside the function
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 16, y - 20))  # Extra change to x and y to adjust the bullet to fire from top of player


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
no_enemies = 6

for i in range(no_enemies):
    enemyImg.append(pygame.image.load('space-ship.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(0, 200))
    enemyX_change.append(1.5)
    enemyY_change.append(30)

def enemy(x, y, i):  # Define a function for enemy
    screen.blit(enemyImg[i], (x, y))


# Collision
def isCollision(x1, y1, x2, y2):
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    if distance < 30:
        return True
    else:
        return False


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 30)
textX = 10
textY = 10

def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (255, 255, 255))  # Type casting integer to string
    screen.blit(score, (x, y))



# create a while loop to exit the program when the close button is clicked
# All the items that have to appear continuously goes inside the infinite while loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movement Mechanics for player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX -= 8
            if event.key == pygame.K_RIGHT:
                playerX += 8
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    laser_sound = mixer.Sound('laser.wav')
                    laser_sound.play()
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)

    # Boundaries of game
    if playerX >= 736:
        playerX = 736
    elif playerX <= 0:
        playerX = 0
    elif playerY >= 536:
        playerY = 536
    elif playerY <= 400:
        playerY = 400
    else:
        pass

    # Movement Mechanics for Enemy
    for i in range(no_enemies - 1):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= 736:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]

        #Game over
        if enemyY[i]>400:
            for j in range(no_enemies):
                enemyY[j]=1000
                game_over_sound = mixer.Sound('game over.wav')
                game_over_sound.play()
                game_over()
                break

        # Collision of enemy and bullet
        collision_enemy = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision_enemy == True:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 450  # To reset the bullet
            bullet_state = 'ready'  # To reset the bullet state
            score_value += 100  # Increase the score
            enemyX[i] = random.randint(0, 736)  # Resets the enemy
            enemyY[i] = random.randint(0, 200)  # Resets the enemy

        enemy(enemyX[i], enemyY[i], i)
        pygame.display.update()

        # RGB - Red,Green,Blue
    # Change background colour
    screen.fill((192, 192, 192))
    pygame.display.update()  # Add after every change or creation to update it

    # Background Image
    screen.blit(background, (0, 0))
    pygame.display.update()

    player(playerX, playerY)  # Calling the player() function - All images should be defined after the fill
    pygame.display.update()

    # Bullet movement
    if bulletY <= 0:  # if condition to fire multiple bullets
        bulletY = 450
        bullet_state = 'ready'
    if bullet_state == 'fire':
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change
        pygame.display.update()

    show_score(textX, textY)
