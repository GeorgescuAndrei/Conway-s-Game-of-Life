import pygame
import numpy as np

# Constants
WIDTH, HEIGHT = 1440, 800 #Size (in pixels) of the game window
GRID_SIZE = 10 #Size (in pixels) of one grid block
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE #Number of rows and columns (relative to the size of the window and size of the grid block)
WHITE, BLACK = (255, 255, 255), (0, 0, 0) #Grid block colors
FONT_SIZE = 24 #Font size of the title

grid = np.zeros((ROWS, COLS), dtype=int) # Initialize the grid with all zeros
generation_counter = 0 #Initialization of the generation counter

#Function that return the number of alive neighbor cells
def count_neighbors(x, y):
    neighbors = [
        grid[i % ROWS, j % COLS]
        for i in range(x - 1, x + 2)
        for j in range(y - 1, y + 2)
        if (i, j) != (x, y)
    ]
    return sum(neighbors)

#Function that modifies the state of all cells and updates the generation counter 
def update_grid():
    global grid, generation_counter
    new_grid = np.copy(grid)
    for i in range(ROWS):
        for j in range(COLS):
            count = count_neighbors(i, j)
            if grid[i, j] == 1 and (count < 2 or count > 3):
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and count == 3:
                new_grid[i, j] = 1
    grid = new_grid
    generation_counter += 1

#Function that places the correct color according to the cell's state
def draw_grid(screen):
    for i in range(ROWS):
        for j in range(COLS):
            color = WHITE if grid[i, j] == 0 else BLACK
            pygame.draw.rect(screen, color, (j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE))

#Function that places text over the grid (used for generation counter)
def draw_text(screen, text, pos):
    font = pygame.font.Font(None, FONT_SIZE)
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, pos)

#Main function that uses the functions above to run the actual game
def main():
    global grid, generation_counter

    #Initializing the game window
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Conway's Game of Life - Paused")

    clock = pygame.time.Clock()

    running = True
    update_enabled = False

    #Main loop that updates the game state, grid, generation counter and title
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Makes the loop end when game window is closed
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: #Changes the cell state when a cell is clicked
                x, y = event.pos
                col = x // GRID_SIZE
                row = y // GRID_SIZE
                grid[row, col] = 1 - grid[row, col]
                generation_counter = 0  # Reset generation counter when a cell is changed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: #Changes the game state when 'SPACE' is pressed 
                    update_enabled = not update_enabled
                elif event.key == pygame.K_r: #Resets the grid when 'r' is pressed
                    grid = np.zeros((ROWS, COLS), dtype=int)
                    update_enabled = False
                    generation_counter = 0  # Reset generation counter when the grid is cleared

        if update_enabled: #Updates the grid if the game is not paused
            update_grid()

        screen.fill(WHITE)
        draw_grid(screen)

        # Draw generation counter in the bottom left corner
        draw_text(screen, f"Generations: {generation_counter}", (10, HEIGHT - 30))

        # Update window title dynamically
        status_text = "Updating" if update_enabled else "Paused"
        pygame.display.set_caption(f"Conway's Game of Life - {status_text}")

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
