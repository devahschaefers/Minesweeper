import sys, pygame
import random
from GameState import GameState
from placementfunctions import topLeft, topRight, bottomLeft, bottomRight, center

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

SPRITE_SIZE = 32
BORDER = 10  # left, right and bottom border
TOP_BORDER = 100  # top border to display info like time high score, flags etc.

GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
PURPLE = (191, 64, 191)

#Events

GAME_LOSE = pygame.USEREVENT + 1
SECOND = pygame.USEREVENT + 2

FONT = "freesansbold.ttf"


def drawtext(game, size, location, txt, placement=topLeft, color = BLACK):
    font = pygame.font.Font(FONT, size)
    text = font.render(txt, True, color)
    textRect = text.get_rect()
    game.screen.blit(text, placement(location, textRect))


def coordinates_to_pixel_loc(postion):  # maybe think of a better name
    postion = list(postion)
    postion[0] = postion[0] * SPRITE_SIZE + BORDER
    postion[1] = postion[1] * SPRITE_SIZE + TOP_BORDER
    return (postion[0], postion[1])




class Tile():  # should proably rewrite some fo the code for tile to have more functunality or store the values in a different data structure
    def __init__(self, x, y, value):  # maxY and maxX are outer posstin of the sprite while x y is where the computer draws them we need max to do some math calculations
        self.x = x
        self.y = y
        self.postion = (x, y)
        self.value = value  # origanly set to 0 this is updated when evalute_values function is run
        self.revealed = False
        self.isFlagged = False
        self.rect = pygame.Rect(coordinates_to_pixel_loc(self.postion),
                                (SPRITE_SIZE, SPRITE_SIZE))
        self.mineClicked = False


class Game():
    def __init__(self, width, height, numMines):
        self.width = width
        self.height = height
        self.numMines = numMines
        self.numFlags = numMines
        self.size = (width * SPRITE_SIZE + 2 * BORDER,
                     height * SPRITE_SIZE + TOP_BORDER + BORDER)
        self.screen = pygame.display.set_mode(self.size)
        self.grid = list()  # a list of tile objects
        self.mines = list()  # contains a list of mine postions
        self.timer = 0
        self.state = GameState.STARTING

    # private methods
    def __available_positions(self):
        output = list()
        for x in range(self.width):
            for y in range(self.height):
                output.append((x, y))
        return output

    def __generateMines(self):
        pygame.time.set_timer(SECOND, 1000)
        row = list()
        # genrate mines postions
        available_positions = self.__available_positions()
        # creates a grid list in which Tile objects or stored a tile object can be accesd through grid[{x postion of tile object}][{y postion of tile object}]
        for i in range(self.numMines):
            mine = random.choice(available_positions)
            available_positions.remove(mine)
            self.mines.append(mine)

        for x in range(self.width):
            for y in range(self.height):
                if (x, y) in self.mines:
                    row.append(Tile(x, y, -1))
                else:
                    row.append(Tile(x, y, 0))

            self.grid.append(row.copy())
            row.clear()

    def check_win(self):
        amount_revelaed = 0
        for collum in self.grid:
            for tile in collum:
                if tile.revealed:
                    amount_revelaed += 1

        if amount_revelaed == (self.width * self.height) - self.numMines:
            self.state = GameState.WON
            return True

        return False

    def __evalute_values(
        self
    ):  # genrate game has to be called before this for the function to work
        for collumn in self.grid:
            for tile in collumn:  # loop through each tile on the board
                if tile.value != -1:
                    for x in range(
                            -1, 2
                    ):  # the change in x for the tile postion we will check
                        if tile.x + x <= self.width - 1 and tile.x + x >= 0:
                            for y in range(
                                    -1, 2
                            ):  # the change in y for the tile postion we will check
                                if tile.y + y <= self.height - 1 and tile.y + y >= 0:
                                    if self.grid[tile.x + x][tile.y +
                                                             y].value == -1:
                                        tile.value += 1

                    # ik it looks a bit weird but this is the easiest way i could think of

    # public methods
    def reveal_empty(self, postion, invalid_positions):
        for y in range(-1, 2):
            for x in range(-1, 2):
                # print(f"depth: {depth} {postion} {(postion[0] + x, postion[1] + y)} invalid_positions {invalid_positions}") -- commented out but keept just inccase we nned it cuz this was anning to write
                newX = postion[0] + x
                newY = postion[1] + y
                if not (newX > self.width - 1 or newX < 0
                        or newY > self.height - 1
                        or newY < 0):  # check we are not outside of the grid
                    tile = self.grid[newX][newY]
                    if tile.value == 0 and not (
                        (newX, newY) in invalid_positions):
                        invalid_positions.append(
                            (newX, newY)
                        )  # this is so we do not get stuck in an infinte loop
                        self.reveal_empty((newX, newY), invalid_positions)
                    else:
                        tile.revealed = True

    def generateGame(self):
        self.__generateMines()
        self.__evalute_values()

    def draw(self):
        screen = self.screen
        for collumn in self.grid:
            for tile in collumn:
                if tile.revealed and not tile.isFlagged:
                    if tile.value == -1:
                        if not tile.mineClicked:
                            screen.blit(img_mine,
                                        coordinates_to_pixel_loc(tile.postion))
                        else:
                            screen.blit(img_mineClicked,
                                        coordinates_to_pixel_loc(tile.postion))
                    elif tile.value == 0:
                        screen.blit(img_emptyGrid,
                                    coordinates_to_pixel_loc(tile.postion))
                    elif tile.value == 1:
                        screen.blit(img_grid1,
                                    coordinates_to_pixel_loc(tile.postion))
                    elif tile.value == 2:
                        screen.blit(img_grid2,
                                    coordinates_to_pixel_loc(tile.postion))
                    elif tile.value == 3:
                        screen.blit(img_grid3,
                                    coordinates_to_pixel_loc(tile.postion))
                    elif tile.value == 4:
                        screen.blit(img_grid4,
                                    coordinates_to_pixel_loc(tile.postion))
                    elif tile.value == 5:
                        screen.blit(img_grid5,
                                    coordinates_to_pixel_loc(tile.postion))
                    elif tile.value == 6:
                        screen.blit(img_grid6,
                                    coordinates_to_pixel_loc(tile.postion))
                    elif tile.value == 7:
                        screen.blit(img_grid7,
                                    coordinates_to_pixel_loc(tile.postion))
                    elif tile.value == 8:
                        screen.blit(img_grid8,
                                    coordinates_to_pixel_loc(tile.postion))

                elif tile.isFlagged == True:
                    screen.blit(img_flag, coordinates_to_pixel_loc(tile.postion))
                else:
                    screen.blit(img_grid, coordinates_to_pixel_loc((tile.x, tile.y)))

        drawtext(self, 50, (BORDER, TOP_BORDER // 4), str(self.timer))
        drawtext(self, 50, (self.size[0] - BORDER, TOP_BORDER // 4), str(self.numFlags), topRight)
        drawtext(self, 10, (BORDER, TOP_BORDER - 5), "You can always press r to start a new game", bottomLeft)
        if self.state != GameState.PLAYING and self.state != GameState.STARTING:
            drawtext(self, 25, (self.size[0] // 2, self.size[1] // 2), "Press r to start a new game", center, PURPLE)

    def endgame(self):  #show all mines and show wrong flags
        if self.state == GameState.LOST:
            for collumn in self.grid:
                for tile in collumn:
                    if tile.value == -1:
                        tile.revealed = True

    def reset(self, numMines):
        self.numMines = numMines
        self.numFlags = numMines
        self.grid = list()  # a list of tile objects
        self.mines = list()  # contains a list of mine postions
        self.timer = 0
        self.generateGame
        self.state = GameState.STARTING

        self.generateGame()


def main_loop():
    width = 10
    height = 10
    numMines = 10
    game = Game(width, height, numMines)  # maybe add user input for this later
    game.generateGame()
    row = 0
    # print game values in console
    for y in range(game.height):
        for x in range(game.width):
            if game.grid[x][y].value == -1:
                print("m", end=" ")
            else:
                print(game.grid[x][y].value, end=" ")
        row += 1
        print("row:", row, end="")
        print('\n')

    running = True
    while running:
        game.check_win()
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset(numMines)

            if event.type == pygame.QUIT: running = False

            if event.type == SECOND:
                print(game.state)
                if game.state == GameState.PLAYING:
                    game.timer += 1

                print(game.timer)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.state == GameState.STARTING:
                    game.state = GameState.PLAYING

                pos = pygame.mouse.get_pos()
                for collumn in game.grid:
                  for tile in collumn:

                      if tile.rect.collidepoint(pos):

                          if event.button == 1 and not tile.isFlagged and game.state == GameState.PLAYING:

                              print(game.state == GameState.PLAYING)

                              if tile.value == 0:
                                  game.reveal_empty(tile.postion, [])

                              if tile.value == -1:
                                  game.state = GameState.LOST
                                  tile.mineClicked = True
                                  pygame.event.post(pygame.event.Event(GAME_LOSE))
                                  game.endgame()

                              tile.revealed = True

                          if event.button == 3 and not tile.revealed and game.state == GameState.PLAYING:

                              if tile.isFlagged:
                                  tile.isFlagged = False
                                  game.numFlags += 1
                              else:
                                  tile.isFlagged = True
                                  game.numFlags -= 1

        game.screen.fill(GRAY)
        game.draw()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main_loop()
