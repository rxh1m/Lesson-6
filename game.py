import pygame, random
pygame.init()

WIDTH = 1000
HEIGHT = 1100

screen = pygame.display.set_mode((WIDTH,HEIGHT))

bg = pygame.image.load("Lesson 6/images/Background.png")
bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))

ground = pygame.image.load("Lesson 6/images/GrassBase.png")
ground = pygame.transform.scale(ground,(WIDTH + 500, 100))

Flappy1 = pygame.image.load("Lesson 6/images/Flappy_1.png")
Flappy2 = pygame.image.load("Lesson 6/images/Flappy_2.png")
Flappy3 = pygame.image.load("Lesson 6/images/Flappy_3.png")

pipe = pygame.image.load("Lesson 6/images/GreenTube.png")

game = True
groundx = 0
flying = True
pipegap = 150
pipefrequency = 1500
last_pipe = pygame.time.get_ticks() - pipefrequency

class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,pos):
        super().__init__()
        self.image = pipe
        self.rect = self.image.get_rect()
        if pos == 1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = [x,y - (pipegap/2)]
        elif pos == -1:
            self.rect.topleft = [x,y + (pipegap/2)]

    def update(self):
        self.rect.x -= 2.6
        if self.rect.right < 0:
            self.kill()
        

class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.frames = [Flappy1,Flappy2,Flappy3]
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = x,y
        self.counter = 0
        self.velocity = 0
        self.click = False

    def update(self):
        if flying == True:
            self.velocity += 0.2
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.bottom < HEIGHT - 100:
                self.rect.y += self.velocity
        if game == True:
            if pygame.mouse.get_pressed()[0] and self.click == False:
                self.click = True
                self.velocity = -6.25
            if pygame.mouse.get_pressed()[0] == 0:
                self.click = False
            self.counter += 1
            if self.counter > 1.5:
                self.index += 1
                if self.index >= 3:
                    self.index = 0
                self.image = self.frames [self.index]

Bobby = Bird(100, HEIGHT/2 - 100)
Bird_group = pygame.sprite.Group()
Bird_group.add(Bobby)

Pipe_group = pygame.sprite.Group()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.QUIT()
        if event.type == pygame.MOUSEBUTTONDOWN and game == True and flying == False:
            flying = True
            
    screen.fill("sky blue")
    screen.blit(bg,(0,0))
    screen.blit(ground,(groundx,HEIGHT - 100))
    if pygame.sprite.groupcollide(Bird_group,Pipe_group,False,False) or Bobby.rect.top < 0:
        game = False
    if game ==  True and flying == True:
        timenow = pygame.time.get_ticks()
        if timenow - last_pipe > pipefrequency:
            ht = random.randint(-100,100)
            btmpipe = Pipe(WIDTH, HEIGHT/2 + ht, -1)
            toppipe = Pipe(WIDTH, HEIGHT/2 + ht, 1)
            Pipe_group.add(btmpipe)
            Pipe_group.add(toppipe)
            last_pipe = timenow
        Pipe_group.update()
        groundx -= 1
        if abs(groundx) > 35:
            groundx = 0
    if Bobby.rect.bottom >= HEIGHT - 100:
        game = False
        flying = False
    Bird_group.draw(screen)
    Bird_group.update()
    Pipe_group.draw(screen)
    pygame.display.update()
