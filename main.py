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
    def __init__(self, x, y, isMine, maxX, maxY):
        self.x = x
        self.y = y
        self.postion = (x, y)
        self.isMine = isMine
        self.value = 0
        if self.isMine:
            self.value = -1


class Game():
    def __init__(self, width, height, numMines):
        self.width = width
        self.height = height
        self.numMines = numMines
        self.size = (width * SPRITE_SIZE + 2 * BORDER, height * SPRITE_SIZE + TOP_BORDER + BORDER)
        self.screen = pygame.display.set_mode(self.size)
        self.grid = list() #a list of tile objects
        self.mines = list() #contains a list of mine postions


    def generateGame(self): #creates a grid list in which Tile objects or stored a tile object can be accesd through grid[{x postion of tile object}][{y postion of tile object}]
        row = list()
        #genrate mines postions
        for i in range(self.numMines):
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            self.mines.append((x, y))

        for x in range(self.width):
            for y in range(self.height):
                if (x, y) in self.mines:
                    row.append(Tile(x, y, True, self.width, self.height))
                else:
                    row.append(Tile(x, y, False, self.width, self.height))
            self.grid.append(row.copy())
            row.clear()

    def evalute_values(self): #genrate game has to be called before this for the function to work
        for row in self.grid:
            for tile in row: # loop through each tile on the board
                if tile.isMine == False:
                    for x in range(-1, 2): #the change in x for the tile postion we will check
                        if tile.x + x <= 9 and tile.x + x >= 0:
                            for y in range(-1, 2): #the change in y for the tile postion we will check
                                if tile.y + y <= 9 and tile.y + y >= 0:
                                    if self.grid[tile.x + x][tile.y + y].isMine:
                                        tile.value += 1



game = Game(10, 10, 9) #maybe add user input for this later
game.generateGame()
game.evalute_values()

for x in range(10):
    print('\n')
    for  y in range(10):
        print(game.grid[x][y].value, end = " ")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    game.screen.fill(GRAY)
    game.screen.blit(spr_flag, (BORDER, TOP_BORDER))
    pygame.display.flip()
