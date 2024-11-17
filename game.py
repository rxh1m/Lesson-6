import pygame
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

game = True
groundx = 0
flying = True

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
            self.velocity += 0.1
            if self.velocity > 8:
                self.velocity = 8
            if self.rect.bottom < HEIGHT - 100:
                self.rect.y += self.velocity
        if game == True:
            if pygame.mouse.get_pressed()[0] and self.click == False:
                self.click = True
                self.velocity = -5
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
    if game ==  True and flying == True:
        groundx -= 1
        if abs(groundx) > 35:
            groundx = 0
    if Bobby.rect.bottom >= HEIGHT - 100:
        game = False
        flying = False
    Bird_group.draw(screen)
    Bird_group.update()
    pygame.display.update()