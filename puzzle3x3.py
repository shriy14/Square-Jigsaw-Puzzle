import pygame
import os
import random

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
GRID_BLOCK_SIZE = 100
PIECE_SIZE = 70
GRID_PADDING = 10
ANS_SIZE = 200

# initialise the window, icon, and logo
pygame.init()
background = pygame.image.load('resources/background.png')
custom_font_path = 'resources/fonts/Dynamo W04 Bold Condensed.ttf'
custom_font = pygame.font.Font(custom_font_path, 40)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

icon = pygame.image.load('resources/icon.png')
main_logo = pygame.image.load('resources/static_logo.png')
main_logo = pygame.transform.scale(main_logo, (250, 100))
pygame.display.set_caption('Puzzle Champ')
pygame.display.set_icon(icon)

# make the empty grid
def drawGrid():
    for x in range(150, 451, GRID_BLOCK_SIZE + GRID_PADDING):
        for y in range(150, 451, GRID_BLOCK_SIZE + GRID_PADDING):
            rect = pygame.Rect(x, y, GRID_BLOCK_SIZE, GRID_BLOCK_SIZE)
            pygame.draw.rect(screen, (0,0,0), rect, 1)

# displaying the final image that needs to be formed
def ans_image():
    rect = pygame.Rect(650, 50, ANS_SIZE, ANS_SIZE)
    pygame.draw.rect(screen, (0,0,0), rect, 1)
    answer_img = pygame.image.load('resources/image1.jpg')
    answer_img = pygame.transform.scale(answer_img, (ANS_SIZE, ANS_SIZE))
    screen.blit(answer_img, (650, 50))

# retrieving the split pieces
puzzle_dir = 'resources/puzzles/3/'
piece_files = [f for f in os.listdir(puzzle_dir) if f.endswith('.jpg')]

# this class gives all the functions related to a puzzle piece
class PuzzlePiece:
    def __init__(self, image, large_image,  pos, name):
        self.original_image = image
        # self.large_image = pygame.transform.scale(image, (GRID_BLOCK_SIZE, GRID_BLOCK_SIZE)) # enlarge image when it reaches the grid
        self.large_image = large_image
        self.image = self.original_image
        self.rect = self.image.get_rect() # area
        self.rect.topleft = pos
        self.name = name
        self.dragging = False
        self.in_grid = False

    def update(self, mouse_pos):
        if self.dragging:
            self.rect.topleft = mouse_pos
            grid_pos = self.get_grid_position(mouse_pos)
            if grid_pos and not self.is_block_occupied(grid_pos):
                self.rect.topleft = grid_pos
                self.image = self.large_image
                self.in_grid = True
            else:
                self.image = self.original_image
                self.in_grid = False
            self.rect.size = self.image.get_size()

    def get_grid_position(self, pos):
        for x in range(150, 451, GRID_BLOCK_SIZE + GRID_PADDING):
            for y in range(150, 451, GRID_BLOCK_SIZE + GRID_PADDING):
                if pygame.Rect(x, y, GRID_BLOCK_SIZE, GRID_BLOCK_SIZE).collidepoint(pos):
                    return (x, y)
        return None

    def is_block_occupied(self, grid_pos):
        for piece in puzzle_pieces:
            if piece != self and piece.in_grid and piece.rect.topleft == grid_pos:
                return True
        return False

#adjust pieces position here

def pieces():
    random.shuffle(piece_files)
    pieces = []
    for i, file in enumerate(piece_files):
        original_image = pygame.image.load(puzzle_dir + file)
        small_image = pygame.transform.scale(original_image, (PIECE_SIZE, PIECE_SIZE))
        large_image = pygame.transform.scale(original_image, (GRID_BLOCK_SIZE, GRID_BLOCK_SIZE))
        x = 625 + i % 3 * (PIECE_SIZE + GRID_PADDING)
        y = 260 + i // 3 * (PIECE_SIZE + GRID_PADDING)
        piece = PuzzlePiece(small_image, large_image, (x, y), file)
        pieces.append(piece)
    return pieces


def check_win(pieces):
    correct_positions = {
        f'{row}_{col}.jpg': (150 + col * (GRID_BLOCK_SIZE + GRID_PADDING), 150 + row * (GRID_BLOCK_SIZE + GRID_PADDING))
        for row in range(3) for col in range(3)
    }
    for piece in pieces:
        if not piece.in_grid or piece.rect.topleft != correct_positions[piece.name]:
            return False
    return True

def draw_button(text, x, y, width, height, inactive_color, active_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x + width > mouse[0] > x and y + height > mouse[1] > y: #hovering condition
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    
    custom_font = pygame.font.Font(custom_font_path, 20)    
    text_surf = custom_font.render(text, True, (255,255,255))
    text_rect = text_surf.get_rect()
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)
    return False

def reset_game():
    global puzzle_pieces, game_over
    puzzle_pieces = pieces()
    game_over = False

running = True
reset_game()
dragging_piece = None
font = pygame.font.Font(None, 36)

while running:
    screen.fill((255, 255, 255))
    
    screen.blit(background, (0,0))
    screen.blit(main_logo, (20, 20))
    drawGrid()
    ans_image()
    
    custom_font_path = 'resources/fonts/Dynamo W04 Bold Condensed.ttf'
    custom_font = pygame.font.Font(custom_font_path, 40)
    
    for piece in puzzle_pieces:
        screen.blit(piece.image, piece.rect)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:  # start dragging (click)
            for piece in puzzle_pieces:
                if piece.rect.collidepoint(event.pos):
                    piece.dragging = True
                    dragging_piece = piece
                    puzzle_pieces.remove(piece)
                    puzzle_pieces.append(piece)  # move the piece to the end of the list (top layer)
                    break
        elif event.type == pygame.MOUSEBUTTONUP and not game_over:  # stop dragging (release)
            if dragging_piece:
                dragging_piece.dragging = False
                if not dragging_piece.in_grid:
                    dragging_piece.rect.topleft = (570 + piece_files.index(dragging_piece.name) % 3 * (PIECE_SIZE + GRID_PADDING), 
                                                   300 + piece_files.index(dragging_piece.name) // 3 * (PIECE_SIZE + GRID_PADDING))
                    dragging_piece.image = dragging_piece.original_image
                    dragging_piece.rect.size = dragging_piece.image.get_size()
                dragging_piece = None
        elif event.type == pygame.MOUSEMOTION and not game_over:
            if dragging_piece:
                dragging_piece.update(event.pos)
    
    if check_win(puzzle_pieces):
        win_text = custom_font.render("You win!", True, (0, 255, 60))
        screen.blit(win_text, (WINDOW_WIDTH // 2 - win_text.get_width() // 2, 50))
        if draw_button("Play Again", WINDOW_WIDTH - 300, WINDOW_HEIGHT - 100, 150, 50, (0,255, 60), (255,255,255)):
            reset_game()
    
    elif all(piece.in_grid for piece in puzzle_pieces) and not check_win(puzzle_pieces):
        wrong_text = font.render("Wrong order! Try again.", True, (255, 0, 0))
        screen.blit(wrong_text, (WINDOW_WIDTH // 2 - wrong_text.get_width() // 2, 50))
        if draw_button("Retry", WINDOW_WIDTH - 150, WINDOW_HEIGHT - 100, 100, 50, (200, 0, 0), (255, 0, 0)):
            reset_game()
    
    pygame.display.update()

pygame.quit()
