from pygame import *
from pygame.sprite import *
from random import randint

# Game constants
screen_color = (250, 250, 250)
score = 0
lives_remaining = 1
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

    def kill(self):
        sound = pygame.mixer.Sound("sounds/points.wav")
        sound.play()
        global score
        if self.isBonusBrick:
            score += 100
        else:
            score += 10
        Sprite.kill(self)

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
    
    def collidedWith(self, target):
        return self.rect.colliderect(target)

    def bounce(self):
        sound = pygame.mixer.Sound("sounds/bounce.wav")
        sound.play()


# Paddle class here
class Paddle(Sprite):
    def __init__(self, init_x = 450, init_y = 420):
        Sprite.__init__(self)
        self.x = init_x
        self.y = init_y
        self.movement_speed = 6
        self.image = pygame.Surface([60, 10])
        self.image.fill((0,39,76))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def get_input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.x -= self.movement_speed
            self.playSound()
        elif key[pygame.K_RIGHT]:
            self.x += self.movement_speed
            self.playSound()

    def update(self):
        self.rect.center = (self.x, self.y)

    def playSound(self):
        sound = pygame.mixer.Sound("sounds/move.wav")
        sound.play()

# Game window
# Start game
pygame.init()
text = font.Font(None, 40)
screen = display.set_mode((900, 450))
screen.fill(screen_color)
display.set_caption('Brandon Breakout')
mouse.set_visible(False)

# Group of bricks
Wall = pygame.sprite.Group()
# Create columns of bricks
for i in range(0, 5):
    # Create rows of bricks
    for j in range(0,9):
        Wall.add(Brick(100 * j + 50, 55 + 25 * i))

# Game objects
Balls = pygame.sprite.Group()
Game_ball = Ball(init_v_x = 50, init_v_y = 50)
Balls.add(Game_ball)
Bumper = Paddle()
sprites = RenderPlain(Wall, Game_ball, Bumper)

# Game loop
while True:

    # Quit game on command
    e = event.poll()
    if e.type == QUIT:
        quit()
        break
    
    # Tell bumper to check keyboard
    Bumper.get_input()

    if Game_ball.collidedWith(Bumper):
        Game_ball.bounce()
        Game_ball.vy *= -1

    # Check left edge
    if Game_ball.x <= 0:
        Game_ball.bounce()
        Game_ball.vx *= -1
    # Check right edge
    if Game_ball.x >= 900:
        Game_ball.bounce()
        Game_ball.vx *= -1
    # Check top edge
    if Game_ball.y <= 50:
        Game_ball.bounce()
        Game_ball.vy *= -1

    # Life loss condition
    if Game_ball.y >= 425:
        sound = pygame.mixer.Sound("sounds/lostLife.wav")
        sound.play()
        pygame.time.delay(3000)
        Game_ball.x = 450
        Game_ball.y = 200
        Game_ball.vx = 50
        Game_ball.vy = 50
        lives_remaining -= 1

    # If ball hits brick
    if pygame.sprite.groupcollide(Balls, Wall, False, True):
        Game_ball.vy *= -1
    
    # Paint background to fill
    screen.fill(screen_color)

    # Scoreboard takes up entire width and 40 pixels of height.
    pygame.draw.rect(screen,(230, 230, 230),(0, 0, 900, 40))
    if lives_remaining >= 0:
        lives_display = text.render("Lives Remaining: " + str(lives_remaining), 1, (0,39,76))
        screen.blit(lives_display, (630, 5))
    else:
        lives_display = text.render("GAME OVER.", 1, (0,39,76))
        screen.blit(lives_display, (700, 5))
    current_score = text.render("Score: " + str(score), 1, (255,203,5))
    screen.blit(current_score, (10, 5))

    # GAME OVER condition
    if lives_remaining == 0:
        sound = pygame.mixer.Sound("sounds/gameOver.wav")
        sound.play()
        sprites.remove(Game_ball)
        sprites.remove(Bumper)
        lives_remaining -= 1

    # Update game objects on each loop
    sprites.update()
    sprites.draw(screen)
    display.update()
