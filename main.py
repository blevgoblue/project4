from pygame import *
from pygame.sprite import *
from random import *

# Game constants
screen_color = (250, 250, 250)
initial_ball_speed = 1
score = 0
lives_remaining = 3
game_clock = pygame.time.Clock()


# Brick class here


# Ball class here


# Paddle class here


# Game window

# Start game
pygame.init()
text = font.Font(None, 40)
screen = display.set_mode((900, 900))
screen.fill(screen_color)
display.set_caption('Brandon Breakout')
mouse.set_visible(False)

# Game loop
while True:
    
    # Quit game on command
    e = event.poll()
    if e.type == QUIT:
        quit()
        break

    lives_display = text.render("Lives Remaining: " + str(lives_remaining), 1, (0,39,76))
    screen.blit(lives_display, (630, 5))

    current_score = text.render("Score: " + str(score), 1, (255,203,5))
    screen.blit(current_score, (10, 5))

    display.update()

