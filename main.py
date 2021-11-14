import sys, pygame, random

pygame.init()

img_emptyGrid = pygame.image.load("Sprites/empty.png")
img_flag = pygame.image.load("Sprites/flag.png")
img_grid = pygame.image.load("Sprites/Grid.png")
img_grid1 = pygame.image.load("Sprites/grid1.png")
img_grid2 = pygame.image.load("Sprites/grid2.png")
img_grid3 = pygame.image.load("Sprites/grid3.png")
img_grid4 = pygame.image.load("Sprites/grid4.png")
img_grid5 = pygame.image.load("Sprites/grid5.png")
img_grid6 = pygame.image.load("Sprites/grid6.png")
img_grid7 = pygame.image.load("Sprites/grid7.png")
img_grid8 = pygame.image.load("Sprites/grid8.png")
img_mine = pygame.image.load("Sprites/mine.png")
img_mineClicked = pygame.image.load("Sprites/mineClicked.png")
img_mineFalse = pygame.image.load("Sprites/mineFalse.png")

SPRITE_SIZE= 32
BORDER = 10 # left, right and bottom border
TOP_BORDER = 100 #top border to display info like time high score, flags etc.

GRAY = (128, 128, 128)

class Tile():
    def __init__(self, x, y, isMine, maxX, maxY):
        self.x = x
        self.y = y
        self.postion = (x, y)
        self.value = 0 #origanly set to 0 this is updated when evalute_values function is run
        self.isMine = isMine
        self.isClicked = False
        self.isFlagged = False


class Game():
    def __init__(self, width, height, numMines):
        self.width = width
        self.height = height
        self.numMines = numMines
        self.size = (width * SPRITE_SIZE + 2 * BORDER, height * SPRITE_SIZE + TOP_BORDER + BORDER)
        self.screen = pygame.display.set_mode(self.size)
        self.grid = list() #a list of tile objects
        self.mines = list() #contains a list of mine postions

    #private methods
    def coordinates_to_pixel_loc(self, postion):
        postion = list(postion)
        postion[0] = postion[0] * SPRITE_SIZE + BORDER
        postion[1] = postion[1] * SPRITE_SIZE + TOP_BORDER
        return (postion[0], postion[1])


    #public methods
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
        for collumn in self.grid:
            for tile in collumn: # loop through each tile on the board
                if tile.isMine == False:
                    for x in range(-1, 2): #the change in x for the tile postion we will check
                        if tile.x + x <= 9 and tile.x + x >= 0:
                            for y in range(-1, 2): #the change in y for the tile postion we will check
                                if tile.y + y <= 9 and tile.y + y >= 0:
                                    if self.grid[tile.x + x][tile.y + y].isMine:
                                        tile.value += 1
                else: tile.value = -1

                                        #ik it looks a bit weird but this is the easiest way i could think of

    def draw(self):
        screen = self.screen
        for collumn in self.grid:
            for tile in collumn:
                if tile.value == -1:
                    screen.blit(img_mine, (self.coordinates_to_pixel_loc((tile.x, tile.y)))) #need to make funtion later and maybe think of a better name
                elif tile.value == 0:
                    screen.blit(img_emptyGrid, self.coordinates_to_pixel_loc((tile.x, tile.y)))
                elif tile.value == 1:
                    screen.blit(img_grid1, self.coordinates_to_pixel_loc((tile.x, tile.y)))
                elif tile.value == 2:
                    screen.blit(img_grid2, self.coordinates_to_pixel_loc((tile.x, tile.y)))
                elif tile.value == 3:
                    screen.blit(img_grid3, self.coordinates_to_pixel_loc((tile.x, tile.y)))
                elif tile.value == 4:
                    screen.blit(img_grid4, self.coordinates_to_pixel_loc((tile.x, tile.y)))
                elif tile.value == 5:
                    screen.blit(img_grid5, self.coordinates_to_pixel_loc((tile.x, tile.y)))
                elif tile.value == 6:
                    screen.blit(img_grid6, self.coordinates_to_pixel_loc((tile.x, tile.y)))
                elif tile.value == 7:
                    screen.blit(img_grid7, self.coordinates_to_pixel_loc((tile.x, tile.y)))
                elif tile.value == 8:
                    screen.blit(img_grid8, self.coordinates_to_pixel_loc((tile.x, tile.y)))




game = Game(10, 10, 15) #maybe add user input for this later
game.generateGame()
game.evalute_values()

#print game in console
for x in range(10):
    print('\n')
    for  y in range(10):
        print(game.grid[x][y].value, end = " ")
#----------------------------------------------------------------

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False

    game.screen.fill(GRAY)
    game.draw()
    pygame.display.flip()

pygame.quit()
