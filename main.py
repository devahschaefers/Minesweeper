import sys, pygame, random

pygame.init()

spr_emptyGrid = pygame.image.load("Sprites/empty.png")
spr_flag = pygame.image.load("Sprites/flag.png")
spr_grid = pygame.image.load("Sprites/Grid.png")
spr_grid1 = pygame.image.load("Sprites/grid1.png")
spr_grid2 = pygame.image.load("Sprites/grid2.png")
spr_grid3 = pygame.image.load("Sprites/grid3.png")
spr_grid4 = pygame.image.load("Sprites/grid4.png")
spr_grid5 = pygame.image.load("Sprites/grid5.png")
spr_grid6 = pygame.image.load("Sprites/grid6.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_grid8 = pygame.image.load("Sprites/grid8.png")
spr_grid7 = pygame.image.load("Sprites/grid7.png")
spr_mine = pygame.image.load("Sprites/mine.png")
spr_mineClicked = pygame.image.load("Sprites/mineClicked.png")
spr_mineFalse = pygame.image.load("Sprites/mineFalse.png")

SPRITE_SIZE= 32
BORDER = 10 # left, right and bottom border
TOP_BORDER = 100 #top border to display info like time high score, flags etc.

GRAY = (128, 128, 128)

class Tile():
    def __init__(self, x, y, isMine):
        self.x = x
        self.y = y
        self.isMine = isMine

class Game():
    def __init__(self, width, height, numMines):
        self.width = width
        self.height = height
        self.numMines = numMines
        self.size = (width * SPRITE_SIZE + 2 * BORDER, height * SPRITE_SIZE + TOP_BORDER + BORDER)
        self.screen = pygame.display.set_mode(self.size)
        self.grid = list() #a list of tile objects
        self.mines = list() #contains a list of mine postions

    def generateGame(self):
        row = list()
        #genrate mines
        for i in range(self.numMines):
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            self.mines.append((x, y))

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.mines:
                    row.append(Tile(x, y, True))
                else:
                    row.append(Tile(x, y, False))
            self.grid.append(row.copy())
            row.clear()






game = Game(10, 10, 9)
game.generateGame()
print(game.mines)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    game.screen.fill(GRAY)
    game.screen.blit(spr_flag, (BORDER, TOP_BORDER))
    pygame.display.flip()
