from pygame import *
from pygame.sprite import *
from random import randint

# Game constants
screen_color = (250, 250, 250)
initial_ball_speed = 1
score = 0
lives_remaining = 3
game_clock = pygame.time.Clock()


# Brick class here.  Bricks are 20 pixels wide by 5 pixels high.
class Brick(Sprite):
    def __init__(self, x_position = 0, y_position = 0):
        Sprite.__init__(self)
        self.isBonusBrick = randint(1,100)
        self.image = pygame.Surface([80, 20])
        self.image.fill(self.decideBrickColor())
        self.rect = self.image.get_rect()
        self.rect.center = (x_position, y_position)
        

    def decideBrickColor(self):
        if self.isBonusBrick <= 10:
            return (0,39,76)
        else:
            return (255, 203, 5)



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

Brick = Brick(45, 55)
sprites = RenderPlain(Brick)

# Game loop
while True:
    
    # Quit game on command
    e = event.poll()
    if e.type == QUIT:
        quit()
        break

    # Scoreboard takes up entire width and 40 pixels of height.
    pygame.draw.rect(screen,(230, 230, 230),(0, 0, 900, 40))
    lives_display = text.render("Lives Remaining: " + str(lives_remaining), 1, (0,39,76))
    screen.blit(lives_display, (630, 5))
    current_score = text.render("Score: " + str(score), 1, (255,203,5))
    screen.blit(current_score, (10, 5))

    # Update game objects on each loop
    sprites.update()
    sprites.draw(screen)
    display.update()

