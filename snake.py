#import and initialize
from button import Button
import pygame
from pygame.locals import *
import random
pygame.init()
pygame.font.init()

#variables
direction = None
positions = [[9,9],[8,9]]
pos_apples = [[14,9]]
can_turn = True
menu = True
show_game_over = False

#game modifiers
field_size = 20
speed_multiplier = 1
amount_of_apples = 1
spawn_blocks = False
blocks = []

#colors
BLACK = (0,  0,  0)
WHITE = (255,  255,  255)
BLUE = (79, 120, 248)
RED = (231, 71, 29)
GREEN = (142, 204, 57)
LIGHT_GREEN = (167, 217, 72)
EXTRA_LIGHT_GREEN = (188, 242, 82)
DARK_GREEN = (107, 153, 42)

#game assets
HEAD_IMG = pygame.transform.scale(pygame.image.load("textures/head.png"), (20, 20))
BOTTOM_IMG = pygame.transform.scale(pygame.image.load("textures/bottom.png"), (20, 20))
APPLE_IMG = pygame.transform.scale(pygame.image.load("textures/apple.png"), (20, 20))

SPEED_DEFAULT_IMG = pygame.image.load("textures/default_speed.png")
SPEED_FAST_IMG = pygame.image.load("textures/fast_speed.png")
SPEED_EXTRA_FAST_IMG = pygame.image.load("textures/extra_fast_speed.png")
SPEED_SLOW_IMG = pygame.image.load("textures/slow_speed.png")

AMOUNT_OF_APPLES_ONE_IMG = pygame.image.load("textures/apple.png")
AMOUNT_OF_APPLES_THREE_IMG = pygame.image.load("textures/three_amount_of_apples.png")
AMOUNT_OF_APPLES_FIVE_IMG = pygame.image.load("textures/five_amount_of_apples.png")
AMOUNT_OF_APPLES_TEN_IMG = pygame.image.load("textures/ten_amount_of_apples.png")

SPAWN_BLOCKS_FALSE_IMG =pygame.image.load("textures/blocks_false.png")
SPAWN_BLOCKS_TRUE_IMG = pygame.image.load("textures/blocks_true.png")

TITLE_FONT = pygame.font.Font("fonts/special_font.ttf", 30)
DEFAULT_FONT = pygame.font.Font("fonts/default_font.ttf", 15)

SPEED_BUTTON = Button(175, 175, 50, 50, [1, 2, 4, 0.5], [SPEED_DEFAULT_IMG, SPEED_FAST_IMG, SPEED_EXTRA_FAST_IMG, SPEED_SLOW_IMG], EXTRA_LIGHT_GREEN)
AMOUNT_OF_APPLES_BUTTON = Button(50, 175, 50, 50, [1, 3, 5, 10], [AMOUNT_OF_APPLES_ONE_IMG, AMOUNT_OF_APPLES_THREE_IMG,AMOUNT_OF_APPLES_FIVE_IMG, AMOUNT_OF_APPLES_TEN_IMG], EXTRA_LIGHT_GREEN)
SPAWN_BLOCKS_BUTTON = Button(300, 175, 50, 50, [False, True], [SPAWN_BLOCKS_FALSE_IMG, SPAWN_BLOCKS_TRUE_IMG], EXTRA_LIGHT_GREEN)

#size window
WINDOW_WIDTH =  400
WINDOW_HEIGHT =  400

#size grid and cells
GRID_SIZE =  20
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE

#initialize a game
def initialize_game(mod_speed = 1, mod_amount_apples = 1, mod_blocks_spawning = False, mod_field_size = 20):
    global can_turn, pos_apples, positions, direction, field_size, speed_multiplier, amount_of_apples, blocks, spawn_blocks

    #positions and booleans
    direction = None
    positions = [[9,9],[8,9]]
    can_turn = True

    #modifiers
    field_size = mod_field_size
    speed_multiplier = mod_speed
    amount_of_apples = mod_amount_apples
    spawn_blocks = mod_blocks_spawning
    blocks = []

    #apple positions
    if amount_of_apples == 3:
        pos_apples = [[15,9],[13,7],[13,11]]
    elif amount_of_apples == 5:
        pos_apples = [[14,9],[12,7],[12,11],[16,7],[16,11]]
    elif amount_of_apples == 10:
        pos_apples = [[14,9],[16,9],[14,7],[16,7],[14,11],[16,11],[12,8],[12,10],[18,8],[18,10]]
    else:
        pos_apples = [[14,9]]

#draw the grid
def draw_grid(window_surface):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(window_surface, GREEN, (x,  0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(window_surface, GREEN, (0, y), (WINDOW_WIDTH, y))

#fill a cell
def fill_cell(window_surface, x, y, color):
    pygame.draw.rect(window_surface, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

#draw an image
def draw_img(window_surface, x, y, img):
    window_surface.blit(img, (x * CELL_SIZE, y * CELL_SIZE))

#calculate the new positions of the snake
def move_snake(direction, positions):
    if direction == "right":
        new = [positions[0][0] + 1,positions[0][1]]
    elif direction == "left":
        new = [positions[0][0] - 1,positions[0][1]]
    elif direction == "down":
        new = [positions[0][0],positions[0][1] + 1]
    elif direction == "up":
        new = [positions[0][0],positions[0][1] - 1]
    positions.insert(0,new)
    #Check if the snake eats an apple
    if not eat_apple(positions):
        positions.pop()
    return positions

#draw the snake
def draw_snake(window_surface, positions, direction):
    for cell in positions:
        #draw head
        if cell == positions[0]:
            #up
            if direction == "up":
                draw_img(window_surface, cell[0], cell[1], HEAD_IMG)
            #down
            elif direction == "down":
                draw_img(window_surface, cell[0], cell[1], pygame.transform.rotate(HEAD_IMG, 180))
            #left
            elif direction == "left":
                draw_img(window_surface, cell[0], cell[1], pygame.transform.rotate(HEAD_IMG, 90))
            #right and None
            else:
                draw_img(window_surface, cell[0], cell[1], pygame.transform.rotate(HEAD_IMG, -90))
        #draw bottom
        elif cell == positions[-1]:
            #left
            if (cell[0] - positions[-2][0]) == 1:
                draw_img(window_surface, cell[0], cell[1], pygame.transform.rotate(BOTTOM_IMG, -90))
            #up
            elif (cell[1] - positions[-2][1]) == 1:
                draw_img(window_surface, cell[0], cell[1], pygame.transform.rotate(BOTTOM_IMG, 180))
            #down
            elif (cell[1] - positions[-2][1]) == -1:
                draw_img(window_surface, cell[0], cell[1], BOTTOM_IMG)
            #right and None
            else:
                draw_img(window_surface, cell[0], cell[1], pygame.transform.rotate(BOTTOM_IMG, 90))
        #draw body
        else:
            fill_cell(window_surface, cell[0], cell[1], BLUE)

#return a new position for the apple
def new_apple(positions, pos_apples, block_positions):
    while True:
        new_pos = [random.randint(0,19),random.randint(0,19)]
        if (not new_pos in positions) and (not new_pos in pos_apples) and (not new_pos in block_positions):
            return new_pos

#draw the apple
def draw_apples(window, positions):
    for apple in positions:
        draw_img(window, apple[0], apple[1], APPLE_IMG)

#checks if the snake eats an apple, and if true, it will assign a new position to that apple
def eat_apple(positions):
    global pos_apples, blocks, spawn_blocks
    for i in range(0, len(pos_apples)):
        if pos_apples[i] in positions:
            pos_apples[i] = new_apple(positions, pos_apples, blocks)
            if spawn_blocks:
                new_block(positions, pos_apples)
            return True
    return False

#create a new block
def new_block(positions, pos_apples):
    global blocks
    if random.choice([False, False, True]):
        while True:
            new_pos = [random.randint(0,19),random.randint(0,19)]
            if (not new_pos in positions) and (not new_pos in pos_apples) and (not new_pos in blocks) and (not new_pos in [ [positions[0][0]+1, positions[0][1]], [positions[0][0]-1, positions[0][1]], [positions[0][0], positions[0][1]+1],[positions[0][0], positions[0][1]-1]]):
                blocks.append(new_pos)
                break

#draw the blocks
def draw_blocks(window, block_positions):
    for block in block_positions:
        fill_cell(window, block[0], block[1], DARK_GREEN)

#check if the snake hits itself  
def hit_snake(positions):
    if positions[0] in positions[1:]:
        game_over()

#check if the snake hits the walls    
def hit_wall(positions):
     if positions[0][0] < 0 or positions[0][0] > 19 or positions[0][1] < 0 or positions[0][1] > 19:
        game_over()

#check if the snakes hits a block
def hit_blocks(positions, block_positions):
    if positions[0] in block_positions:
        game_over()

#game over    
def game_over():
    global menu, show_game_over
    menu = True
    show_game_over = True

#write text in the title font
def write_title_text(window_surface, text, color, y):
    text_size = TITLE_FONT.size(text)
    window_surface.blit(TITLE_FONT.render(text, False, color), ( (WINDOW_WIDTH/2) - (text_size[0]/2) , y))

#write text in the default font
def write_default_text(window_surface, text, color, y, background = False, background_color = (0, 0, 0)):
    text_size = DEFAULT_FONT.size(text)
    if background:
        rect = pygame.Rect( (WINDOW_WIDTH/2) - (text_size[0]/2) - 15, y - 15, text_size[0] + 30, text_size[1] + 30)
        pygame.draw.rect(window_surface, background_color, rect)
    window_surface.blit(DEFAULT_FONT.render(text, False, color), ( (WINDOW_WIDTH/2) - (text_size[0]/2) , y))

#game loop
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
running = True
while running:
    
    #events
    for event in pygame.event.get(): 
        #quit
        if event.type == pygame.QUIT:
            running = False
        #button events
        elif event.type == pygame.KEYDOWN:
            #change direction
            if not menu:
                if event.key == K_RIGHT:
                    if can_turn and not direction == "left":
                        direction="right"
                        can_turn = False
                elif event.key == K_UP:
                    if can_turn and not direction == "down":
                        direction="up"
                        can_turn = False
                elif event.key == K_LEFT:
                    if can_turn and not direction == "right":
                        direction="left"
                        can_turn = False
                elif event.key == K_DOWN:
                    if can_turn and not direction == "up":
                        direction="down"
                        can_turn = False
            elif not show_game_over:
                #start game
                if event.key == K_SPACE:
                    initialize_game(SPEED_BUTTON._return(), AMOUNT_OF_APPLES_BUTTON._return(), SPAWN_BLOCKS_BUTTON._return())
                    menu = False
            else:
                #go to menu
                if event.key == K_SPACE:
                    show_game_over = False
        #mouseclick
        elif event.type == pygame.MOUSEBUTTONUP:
            #check if the buttons are clicked
            if menu:
                mouse_pos = pygame.mouse.get_pos()
                SPEED_BUTTON.clicked(mouse_pos)
                AMOUNT_OF_APPLES_BUTTON.clicked(mouse_pos)
                SPAWN_BLOCKS_BUTTON.clicked(mouse_pos)


    #game
    if not menu:
        can_turn = True
        
        #fill background
        window.fill(LIGHT_GREEN)

        #draw apple
        draw_apples(window, pos_apples)

        #move the snake
        if not direction == None:
            positions = move_snake(direction, positions)
        
        #check if snake hits something
        hit_snake(positions)
        hit_wall(positions)
        hit_blocks(positions, blocks)

        #draw snake
        draw_snake(window, positions, direction)

        #draw blocks
        draw_blocks(window, blocks)
    
        #draw grid
        draw_grid(window)  
    
    #menu
    elif not show_game_over:
        #fill background
        window.fill(GREEN)

        #draw the logo
        write_title_text(window, "SNAKE", BLUE, 50)

        #draw the start button
        write_default_text(window, "Press [SPACE] to start", DARK_GREEN, 330, True, EXTRA_LIGHT_GREEN)

        #buttons
        SPEED_BUTTON.draw(window)
        AMOUNT_OF_APPLES_BUTTON.draw(window)
        SPAWN_BLOCKS_BUTTON.draw(window)
    
    #game over screen
    else:
        #fill background
        window.fill(GREEN)

        #draw "GAME OVER"
        write_title_text(window, "GAME OVER", RED, 50)

        #write "SCORE:"
        write_default_text(window, "SCORE:", EXTRA_LIGHT_GREEN, 150)

        #write the score
        write_title_text(window, str( len(positions) - 2 ), BLUE, 180)

        #the button to return to the main menu
        write_default_text(window, "Press [SPACE] to return to the main menu", DARK_GREEN, 330, True, EXTRA_LIGHT_GREEN)

    #finish game tick
    pygame.display.flip()
    if menu:
        pygame.time.delay(100)
    else:
        pygame.time.delay( int( 300 / speed_multiplier ) )
    
pygame.quit()