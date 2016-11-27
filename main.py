from pygame import *
from pygame.sprite import *
from random import randint

# Game constants
screen_color = (250, 250, 250)
score = 0
lives_remaining = 3
game_clock = pygame.time.Clock()


# Brick class here.  Bricks are 80 pixels wide by 20 pixels high.
class Brick(Sprite):
    def __init__(self, x_position = 0, y_position = 0):
        Sprite.__init__(self)
        if randint(1,100) <= 10:
            self.isBonusBrick = True
        else:
            self.isBonusBrick = False
        self.image = pygame.Surface([80, 20])
        self.image.fill(self.decideBrickColor())
        self.rect = self.image.get_rect()
        self.rect.center = (x_position, y_position)
        

    def decideBrickColor(self):
        if self.isBonusBrick:
            return (255, 203, 5)
        else:
            return (0,39,76)

# Ball class here
class Ball(Sprite):
    def __init__(self, init_x = 450, init_v_x = 0, init_y = 200, init_v_y = 0):
        self.x = init_x
        self.y = init_y
        self.vx = init_v_x
        self.vy = init_v_y
        Sprite.__init__(self)
        self.image=pygame.Surface((30,30))
        self.image.fill(screen_color)
        pygame.draw.circle(self.image,(255,0,0),(15,15),15,0)
        self.rect=self.image.get_rect()
    def update(self):
        self.x += self.vx / 30
        self.y += self.vy / 30
        self.rect.center = (self.x, self.y)

# Paddle class here
class Paddle(Sprite):
    def __init__(self, init_x = 450, init_y = 420):
        Sprite.__init__(self)
        self.x = init_x
        self.y = init_y
        self.movement_speed = 6
        self.image = pygame.Surface([60, 10])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def get_input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.x -= self.movement_speed
        elif key[pygame.K_RIGHT]:
            self.x += self.movement_speed

    def update(self):
        self.rect.center = (self.x, self.y)

# Game window
# Start game
pygame.init()
text = font.Font(None, 40)
screen = display.set_mode((900, 450))
screen.fill(screen_color)
display.set_caption('Brandon Breakout')
mouse.set_visible(False)

# Generate row of bricks
Wall = pygame.sprite.Group()
for i in range(0, 5):
    for j in range(0,9):
        Wall.add(Brick(100 * j + 50, 55 + 25 * i))

Game_ball = Ball(init_v_x = 50, init_v_y = 50)
Bumper = Paddle()
sprites = RenderPlain(Wall, Game_ball, Bumper)

# Game loop
while True:

    # Quit game on command
    e = event.poll()
    if e.type == QUIT:
        quit()
        break

    Bumper.get_input()

    screen.fill(screen_color)
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

