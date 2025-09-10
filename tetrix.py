import pygame
import random

pygame.init()

# Constants
BLOCK_SIZE = 20
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * (GRID_WIDTH + 8)
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
GRAY = (128, 128, 128)

# Shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]]
]

# Colors for shapes
COLORS = [
    CYAN,
    RED,
    GREEN,
    BLUE,
    ORANGE,
    YELLOW,
    PURPLE
]

class Figura:
    def __init__(self):
        self.shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = [row[:] for row in SHAPES[self.shape_idx]]
        self.color = COLORS[self.shape_idx]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotar(self):
        self.shape = [[self.shape[y][x] for y in range(len(self.shape) - 1, -1, -1)] for x in range(len(self.shape[0]))]

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.figura = Figura()
        self.next_shape = Figura()
        self.gameover = False
        self.score = 0
        self.fall_time = 0
        self.fallspeed = 500
        self.font = pygame.font.Font(None, 36)

    def valid_move(self, figura, x, y):
        for i in range(len(figura.shape)):
            for j in range(len(figura.shape[0])):
                if figura.shape[i][j] == 1:
                    if not (0 <= x + j < GRID_WIDTH and 0 <= y + i < GRID_HEIGHT and self.grid[y + i][x + j] == BLACK):
                        return False
        return True

    def lock_piece(self, figura):
        for i in range(len(figura.shape)):
            for j in range(len(figura.shape[i])):
                if figura.shape[i][j]:
                    if figura.y + i <= 0:
                        self.gameover = True
                        return
                    self.grid[figura.y + i][figura.x + j] = figura.color
        if not self.gameover:
            self.clear_lines()
            self.figura = self.next_shape
            self.next_shape = Figura()

            for i in range(len(self.figura.shape)):
                for j in range(len(self.figura.shape[i])):
                    if self.figura.shape[i][j] and self.grid[self.figura.y + i][self.figura.x + j] != BLACK:
                        self.gameover = True
                        return

    def clear_lines(self):
        lines_cleared = 0
        for i in range(len(self.grid)):
            if all(cell != BLACK for cell in self.grid[i]):
                lines_cleared += 1
                del self.grid[i]
                self.grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        if lines_cleared > 0:
            self.score += (100 * lines_cleared * lines_cleared)

    def draw_grid(self):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                pygame.draw.rect(self.screen, self.grid[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.screen, GRAY, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        for i in range(len(self.figura.shape)):
            for j in range(len(self.figura.shape[i])):
                if self.figura.shape[i][j]:
                    pygame.draw.rect(self.screen, self.figura.color, ((self.figura.x + j) * BLOCK_SIZE, (self.figura.y + i) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        next_piece_text = self.font.render("Siguiente", True, WHITE)
        self.screen.blit(next_piece_text, (GRID_WIDTH * BLOCK_SIZE + 20, 20))
        for i in range(len(self.next_shape.shape)):
            for j in range(len(self.next_shape.shape[i])):
                if self.next_shape.shape[i][j]:
                    pygame.draw.rect(self.screen, self.next_shape.color, (GRID_WIDTH * BLOCK_SIZE + 20 + j * BLOCK_SIZE, 80 + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (GRID_WIDTH * BLOCK_SIZE + 20, 200))

    def run(self):
        while not self.gameover:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.figura.x -= 1
                        if not self.valid_move(self.figura, self.figura.x, self.figura.y):
                            self.figura.x += 1
                    elif event.key == pygame.K_RIGHT:
                        self.figura.x += 1
                        if not self.valid_move(self.figura, self.figura.x, self.figura.y):
                            self.figura.x -= 1
                    elif event.key == pygame.K_UP:
                        self.figura.rotar()
                        if not self.valid_move(self.figura, self.figura.x, self.figura.y):
                            self.figura.rotar()
                    elif event.key == pygame.K_DOWN:
                        self.figura.y += 1
                        if not self.valid_move(self.figura, self.figura.x, self.figura.y):
                            self.figura.y -= 1

            if self.fall_time > self.fallspeed:
                self.fall_time = 0
                self.figura.y += 1
                if not self.valid_move(self.figura, self.figura.x, self.figura.y):
                    self.figura.y -= 1
                    self.lock_piece(self.figura)

            self.screen.fill(BLACK)
            self.draw_grid()
            pygame.display.flip()

        gameover = True

        while gameover:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameover = False
            dark_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            dark_surface.fill(BLACK)
            dark_surface.set_alpha(128)
            self.screen.blit(dark_surface, (0, 0))

            gameover_text = self.font.render("Game Over", True, WHITE)
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            continue_text = self.font.render("Press x key to exit", True, WHITE)

            text_y = SCREEN_HEIGHT // 2 - 60
            for text in [gameover_text, score_text, continue_text]:
                self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, text_y))
                text_y += 40

            pygame.display.flip()

if __name__ == "__main__":
    game = TetrisGame()
    game.run()

    pygame.quit()